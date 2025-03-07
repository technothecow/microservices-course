import os
import jwt
from datetime import datetime, UTC


def generate_token(user_id: int, expires_in: int = 3600) -> str:
    secret_key = os.getenv("JWT_SECRET_KEY", "secretsecretsecretsecretsecretsecret")
    expires_at = datetime.now(UTC).timestamp() + expires_in
    return jwt.encode(
        {"user_id": user_id, "expires_at": expires_at}, secret_key, algorithm="HS256"
    )

def decode_token(token: str) -> dict:
    secret_key = os.getenv("JWT_SECRET_KEY", "secretsecretsecretsecretsecretsecret")
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        if decoded["expires_at"] < datetime.now(UTC).timestamp():
            raise jwt.ExpiredSignatureError("Token has expired")
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")