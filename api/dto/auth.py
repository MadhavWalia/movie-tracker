from pydantic import BaseModel


class UserRegisteredResponse(BaseModel):
    """
    User Registration Response Model
    """

    user_id: str


class TokenResponse(BaseModel):
    """
    Access Token Response Model
    """

    access_token: str
    refresh_token: str
    token_type: str
