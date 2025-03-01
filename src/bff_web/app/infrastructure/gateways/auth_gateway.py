import jwt
from jwt import PyJWTError

SECRET_KEY = "URG%36!K4b0D3jeWUIhgRMcTTk8qi5ej"
ALGORITHM = "HS256"

def validate_jwt(token: str) -> bool:
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except PyJWTError:
        return False


