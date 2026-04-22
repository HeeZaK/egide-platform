from datetime import datetime, timedelta, timezone

from jose import jwt

_MIN_SECRET_LEN = 32


def create_service_token(secret: str, audience: str, ttl_minutes: int = 15) -> str:
    """
    Génère un JWT HS256 court-vécu pour les appels inter-services.

    Sécurité :
        - Le secret doit faire au minimum 32 caractères (256 bits) pour
          résister au brute-force HMAC. Une ValueError est levée sinon.
        - Le TTL par défaut est de 15 minutes ; ne pas dépasser 60 minutes.
    """
    # FIX: validation longueur minimale du secret HS256
    if len(secret) < _MIN_SECRET_LEN:
        raise ValueError(
            f"Le secret HS256 doit faire au minimum {_MIN_SECRET_LEN} caractères "
            f"(reçu : {len(secret)} caractères). "
            "Utilisez une clé aléatoire de 32+ octets (ex: openssl rand -hex 32)."
        )
    now = datetime.now(timezone.utc)
    payload = {
        "aud": audience,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ttl_minutes)).timestamp()),
    }
    return jwt.encode(payload, secret, algorithm="HS256")
