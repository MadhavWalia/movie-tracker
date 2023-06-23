from pydantic import BaseModel


class UserRegisteredResponse(BaseModel):
    """
    User Registration Response Model
    """

    user_id: str


class AccessTokenResponse(BaseModel):
    """
    Access Token Response Model
    """

    access_token: str
    token_type: str
