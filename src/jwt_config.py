import secrets

# Default cryptographic settings for JWT
DEFAULT_ALGORITHM = "HS256"
DEFAULT_EXPIRATION_MINUTES = 60


def generate_secret_key() -> str:
    # Generates a secure random secret key for JWT signing.
    return secrets.token_hex(32)
