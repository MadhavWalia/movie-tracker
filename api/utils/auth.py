from jose import jwt
from api.settings.auth import JWTSettings
from datetime import datetime, timedelta


def create_access_token(username: str) -> str:
    """
    Create an access token for the user
    """

    # Getting the secret key and algorithm from the settings
    jwtsettings = JWTSettings.get_settings()
    print(jwtsettings)

    # Creating the payload
    exipry = datetime.utcnow() + timedelta(
        minutes=jwtsettings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": username, "exp": exipry}

    # Creating the token
    token = jwt.encode(payload, jwtsettings.SECRET_KEY, jwtsettings.ALGORITHM)

    # Returning the token
    return token
