from datetime import datetime, timedelta, timezone

from jose import jwt


def create_service_token(secret: str, audience: str, ttl_minutes: int = 15) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "aud": audience,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ttl_minutes)).timestamp()),
    }
    return jwt.encode(payload, secret, algorithm="HS256")
