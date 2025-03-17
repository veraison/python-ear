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


# EXAMPLE USAGE

# Generate a secret key
# secret_key = generate_secret_key()
# print(f"Generated Secret Key: {secret_key}")

# # Create an AttestationResult object
# attestation_result = AttestationResult(
#     profile="test_profile",
#     issued_at=int(datetime.timestamp(datetime.now())),
#     verifier_id=VerifierID(developer="Acme Inc.", build="v1"),
#     submods={
#         "submod1": {
#             "trust_vector": TrustVector(instance_identity=UNRECOGNIZED_INSTANCE_CLAIM), # noqa: E501 # pylint: disable=line-too-long
#             "status": TRUST_TIER_AFFIRMING,
#         },
#         "submod2": {
#             "trust_vector": TrustVector(instance_identity=TRUSTWORTHY_INSTANCE_CLAIM), # noqa: E501 # pylint: disable=line-too-long
#             "status": TRUST_TIER_CONTRAINDICATED,
#         },
#     },
# )

# # Print the original AttestationResult object
# print("\n Original AttestationResult Dictionary - JSON:")
# print(json.dumps(attestation_result.to_dict(), indent=4))

# print("\n Original AttestationResult Dictionary - CBOR:")
# print(json.dumps(attestation_result.to_cbor(), indent=4))

# # Sign the AttestationResult and generate a JWT
# jwt_token = sign_ear_claims(attestation_result, secret_key)
# print("\n Signed JWT Token:")
# print(jwt_token)

# # Decode and verify the JWT
# decoded_claims = decode_ear_claims(jwt_token, secret_key)
# print("\n Decoded AttestationResult Dictionary:")
# print(json.dumps(decoded_claims.to_dict(), indent=4))


# OUTPUT

# Generated Secret Key: dadb1756080cabf4c0...d097a705b39c259be3d3

#  Original AttestationResult Dictionary - JSON:
# {
#     "eat_profile": "test_profile",
#     "iat": 1742225266,
#     "ear.verifier-id": {
#         "developer": "Acme Inc.",
#         "build": "v1"
#     },
#     "submods": {
#         "submod1": {
#             "trust_vector": {
#                 "instance_identity": {
#                     "value": 97,
#                     "tag": "unrecognized_instance",
#                     "short": "not recognized",
#                     "long": "The Attesting Environment is not recognized; however the Verifier believes it should be." # noqa: E501 # pylint: disable=line-too-long
#                 },
#                 "configuration": null,
#                 "executables": null,
#                 "file_system": null,
#                 "hardware": null,
#                 "runtime_opaque": null,
#                 "storage_opaque": null,
#                 "sourced_data": null
#             },
#             "status": 2
#         },
#         "submod2": {
#             "trust_vector": {
#                 "instance_identity": {
#                     "value": 2,
#                     "tag": "recognized_instance",
#                     "short": "recognized and not compromised",
#                     "long": "The Attesting Environment is recognized, and the associated instance of the Attester is not known to be compromised." # noqa: E501 # pylint: disable=line-too-long
#                 },
#                 "configuration": null,
#                 "executables": null,
#                 "file_system": null,
#                 "hardware": null,
#                 "runtime_opaque": null,
#                 "storage_opaque": null,
#                 "sourced_data": null
#             },
#             "status": 96
#         }
#     }
# }

#  Original AttestationResult Dictionary - CBOR:
# {
#     "265": "test_profile",
#     "6": 1742225266,
#     "1004": {
#         "0": "Acme Inc.",
#         "1": "v1"
#     },
#     "266": {
#         "submod1": {
#             "1001": {
#                 "0": {
#                     "value": 97,
#                     "tag": "unrecognized_instance",
#                     "short": "not recognized",
#                     "long": "The Attesting Environment is not recognized; however the Verifier believes it should be." # noqa: E501 # pylint: disable=line-too-long
#                 }
#             },
#             "1000": 2
#         },
#         "submod2": {
#             "1001": {
#                 "0": {
#                     "value": 2,
#                     "tag": "recognized_instance",
#                     "short": "recognized and not compromised",
#                     "long": "The Attesting Environment is recognized, and the associated instance of the Attester is not known to be compromised." # noqa: E501 # pylint: disable=line-too-long
#                 }
#             },
#             "1000": 96
#         }
#     }
# }

#  Signed JWT Token:
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...Nq0aWU0BDg

#  Decoded AttestationResult Dictionary:
# {
#     "eat_profile": "test_profile",
#     "iat": 1742225266,
#     "ear.verifier-id": {
#         "developer": "Acme Inc.",
#         "build": "v1"
#     },
#     "submods": {
#         "submod1": {
#             "trust_vector": {
#                 "instance_identity": {
#                     "value": 97,
#                     "tag": "unrecognized_instance",
#                     "short": "not recognized",
#                     "long": "The Attesting Environment is not recognized; however the Verifier believes it should be." # noqa: E501 # pylint: disable=line-too-long
#                 },
#                 "configuration": null,
#                 "executables": null,
#                 "file_system": null,
#                 "hardware": null,
#                 "runtime_opaque": null,
#                 "storage_opaque": null,
#                 "sourced_data": null
#             },
#             "status": 2
#         },
#         "submod2": {
#             "trust_vector": {
#                 "instance_identity": {
#                     "value": 2,
#                     "tag": "recognized_instance",
#                     "short": "recognized and not compromised",
#                     "long": "The Attesting Environment is recognized, and the associated instance of the Attester is not known to be compromised." # noqa: E501 # pylint: disable=line-too-long
#                 },
#                 "configuration": null,
#                 "executables": null,
#                 "file_system": null,
#                 "hardware": null,
#                 "runtime_opaque": null,
#                 "storage_opaque": null,
#                 "sourced_data": null
#             },
#             "status": 96
#         }
#     }
# }
