from pydantic import BaseModel, ConfigDict


class GoogleLoginRequest(BaseModel):
    id_token: str


class UserSettingsResponse(BaseModel):
    default_currency: str
    locale: str
    timezone: str
    dashboard_config: dict
    notification_preferences: dict

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: str
    email: str
    display_name: str
    role: str
    status: str
    personal_context_id: str
    settings: UserSettingsResponse


class AuthResponse(BaseModel):
    user: UserResponse
    csrf_token: str


class MessageResponse(BaseModel):
    message: str
