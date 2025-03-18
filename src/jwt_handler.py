import secrets
from datetime import datetime, timedelta
from typing import Any, Dict

from jose import jwt  # type: ignore # pylint: disable=import-error

from src.claims import AttestationResult

# Default cryptographic settings
DEFAULT_ALGORITHM = "HS256"
DEFAULT_EXPIRATION_MINUTES = 60


def generate_secret_key() -> str:
    # Generates a secure random secret key for JWT signing.
    return secrets.token_hex(32)


def sign_ear_claims(
    ear_claims: AttestationResult,
    secret_key: str,
    algorithm: str = DEFAULT_ALGORITHM,
    expiration_minutes: int = DEFAULT_EXPIRATION_MINUTES,
) -> str:

    # Signs an AttestationResult object and returns a JWT.
    payload = ear_claims.to_dict()
    payload["exp"] = int(
        datetime.timestamp(datetime.now() + timedelta(minutes=expiration_minutes))
    )
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def verify_ear_claims(
    token: str, secret_key: str, algorithm: str = DEFAULT_ALGORITHM
) -> Dict[str, Any]:

    # Verifies a JWT and returns the decoded AttestationResult payload.
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except Exception as exc:
        raise ValueError(f"JWT decoding failed: {exc}") from exc


def decode_ear_claims(
    token: str, secret_key: str, algorithm: str = DEFAULT_ALGORITHM
) -> AttestationResult:

    # Decodes and reconstructs an AttestationResult object from a JWT.
    payload = verify_ear_claims(token, secret_key, algorithm)
    return AttestationResult.from_dict(payload)
