from jose import jwt
from api.settings.auth import JWTSettings
from datetime import datetime, timedelta


def create_access_token(username: str) -> str:
    """
    Create an access token for the user
    """

    # Getting the secret key and algorithm from the settings
    jwtsettings = JWTSettings.get_settings()

    # Creating the payload
    exipry = datetime.utcnow() + timedelta(
        minutes=jwtsettings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": username, "exp": exipry}

    # Creating the token
    access_token = jwt.encode(payload, jwtsettings.SECRET_KEY, jwtsettings.ALGORITHM)

    # Returning the token
    return access_token


def create_refresh_token(username: str) -> str:
    """
    Create a refresh token for the user
    """

    # Getting the secret key and algorithm from the settings
    jwtsettings = JWTSettings.get_settings()

    # Creating the payload
    exipry = datetime.utcnow() + timedelta(
        minutes=jwtsettings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": username, "exp": exipry}

    # Creating the token
    refresh_token = jwt.encode(payload, jwtsettings.SECRET_KEY, jwtsettings.ALGORITHM)

    # Returning the token
    return refresh_token


def decode_token(token: str) -> dict:
    """
    Decode the access token
    """

    # Getting the secret key and algorithm from the settings
    jwtsettings = JWTSettings.get_settings()

    # Decoding the token
    payload = jwt.decode(token, jwtsettings.SECRET_KEY, jwtsettings.ALGORITHM)

    # Returning the payload
    return payload
