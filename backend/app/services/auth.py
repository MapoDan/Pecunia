import hashlib
import hmac
import secrets
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import timedelta

from fastapi import Depends, Header, HTTPException, Request, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import settings
from app.db.session import get_db
from app.models.identity import AccountStatus, AuditEvent, AuthSession, SessionStatus, User, UserSettings, utcnow


@dataclass(frozen=True)
class GoogleIdentity:
    subject: str
    email: str
    display_name: str


def _hash_secret(value: str) -> str:
    return hmac.new(settings.session_secret.encode(), value.encode(), hashlib.sha256).hexdigest()


class GoogleTokenVerifier:
    def verify(self, id_token: str) -> GoogleIdentity:
        if not settings.google_client_id:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Google OAuth is not configured")
        query = urllib.parse.urlencode({"id_token": id_token})
        with urllib.request.urlopen(f"https://oauth2.googleapis.com/tokeninfo?{query}", timeout=5) as response:
            payload = response.read()
        import json

        claims = json.loads(payload)
        if claims.get("aud") != settings.google_client_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google token audience")
        if claims.get("email_verified") not in (True, "true", "True"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Google email is not verified")
        subject = claims.get("sub")
        email = claims.get("email")
        if not subject or not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google identity")
        return GoogleIdentity(subject=subject, email=email, display_name=claims.get("name") or email)


def get_google_verifier() -> GoogleTokenVerifier:
    return GoogleTokenVerifier()


def get_or_create_user(db: Session, identity: GoogleIdentity) -> User:
    user = db.scalar(select(User).where(User.google_subject == identity.subject).options(selectinload(User.settings)))
    if user is None:
        user = User(google_subject=identity.subject, email=identity.email, display_name=identity.display_name)
        user.settings = UserSettings()
        db.add(user)
        db.flush()
        db.add(AuditEvent(actor_user_id=user.id, event_type="identity.user_created", metadata_json={"provider": "google"}))
    else:
        user.email = identity.email
        user.display_name = identity.display_name
        if user.settings is None:
            user.settings = UserSettings()
    return user


def issue_session(db: Session, user: User, response: Response) -> str:
    raw_token = secrets.token_urlsafe(48)
    csrf_token = secrets.token_urlsafe(32)
    session = AuthSession(
        user_id=user.id,
        token_hash=_hash_secret(raw_token),
        csrf_token_hash=_hash_secret(csrf_token),
        expires_at=utcnow() + timedelta(minutes=settings.session_ttl_minutes),
    )
    db.add(session)
    db.add(AuditEvent(actor_user_id=user.id, event_type="identity.session_created", metadata_json={}))
    response.set_cookie(
        settings.session_cookie_name,
        raw_token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=settings.session_ttl_minutes * 60,
        path="/",
    )
    return csrf_token


def user_to_response(user: User) -> dict[str, object]:
    return {
        "id": str(user.id),
        "email": user.email,
        "display_name": user.display_name,
        "role": user.role.value,
        "status": user.status.value,
        "personal_context_id": str(user.personal_context_id),
        "settings": {
            "default_currency": user.settings.default_currency,
            "locale": user.settings.locale,
            "timezone": user.settings.timezone,
            "dashboard_config": user.settings.dashboard_config,
            "notification_preferences": user.settings.notification_preferences,
        },
    }


def current_user(request: Request, db: Session = Depends(get_db)) -> User:
    raw_token = request.cookies.get(settings.session_cookie_name)
    if not raw_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    session = db.scalar(
        select(AuthSession)
        .where(AuthSession.token_hash == _hash_secret(raw_token), AuthSession.status == SessionStatus.active)
        .options(selectinload(AuthSession.user).selectinload(User.settings))
    )
    if session is None or session.expires_at <= utcnow() or session.user.status != AccountStatus.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return session.user


def require_csrf(request: Request, x_csrf_token: str | None = Header(default=None), db: Session = Depends(get_db)) -> AuthSession:
    raw_token = request.cookies.get(settings.session_cookie_name)
    if not raw_token or not x_csrf_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token required")
    session = db.scalar(select(AuthSession).where(AuthSession.token_hash == _hash_secret(raw_token), AuthSession.status == SessionStatus.active))
    if session is None or not hmac.compare_digest(session.csrf_token_hash, _hash_secret(x_csrf_token)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CSRF token")
    return session


def revoke_current_session(response: Response, session: AuthSession, db: Session) -> None:
    session.status = SessionStatus.revoked
    session.revoked_at = utcnow()
    db.add(AuditEvent(actor_user_id=session.user_id, event_type="identity.session_revoked", metadata_json={}))
    response.delete_cookie(settings.session_cookie_name, path="/")
