from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.identity import AuthSession, User
from app.schemas.auth import AuthResponse, GoogleLoginRequest, MessageResponse, UserResponse
from app.services.auth import current_user, get_google_verifier, get_or_create_user, issue_session, require_csrf, revoke_current_session, user_to_response, GoogleTokenVerifier

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/google", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def google_login(payload: GoogleLoginRequest, response: Response, db: Session = Depends(get_db), verifier: GoogleTokenVerifier = Depends(get_google_verifier)) -> dict[str, object]:
    identity = verifier.verify(payload.id_token)
    user = get_or_create_user(db, identity)
    csrf_token = issue_session(db, user, response)
    db.commit()
    db.refresh(user)
    return {"user": user_to_response(user), "csrf_token": csrf_token}


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(current_user)) -> dict[str, object]:
    return user_to_response(user)


@router.post("/logout", response_model=MessageResponse)
def logout(response: Response, session: AuthSession = Depends(require_csrf), db: Session = Depends(get_db)) -> dict[str, str]:
    revoke_current_session(response, session, db)
    db.commit()
    return {"message": "Logged out"}
