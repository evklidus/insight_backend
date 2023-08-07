from http.client import HTTPException
from pstats import Stats
from smtplib import SMTPException
import statistics
from jose import JWTError, jwt

from ...core.services.auth_service import ALGORITHM, SECRET_KEY


def decode_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = decoded_token.get("sub")
        if username is None:
            raise SMTPException(
                status_code=statistics.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        token_data = {"token": token, "username": username}
    except JWTError:
        raise HTTPException(
            status_code=Stats.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    return token_data
