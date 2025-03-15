from typing import Any, Dict

from src.claims import EARClaims
from src.trust_claims import TrustClaim
from src.trust_tier import TrustTier, TrustTierNone, to_trust_tier
from src.trust_vector import TrustVector
from src.verifier_id import VerifierID


class EARValidationError(Exception):
    # Custom exception for validation errors in EARClaims
    pass


def validate_trust_claim(trust_claim: TrustClaim):
    # Validates a TrustClaim object
    if not isinstance(trust_claim.value, int) or not -128 <= trust_claim.value <= 127:
        raise EARValidationError(
            f"Invalid value in TrustClaim: {trust_claim.value}. Must be in range [-128, 127]"
        )
    if not isinstance(trust_claim.tag, str):
        raise EARValidationError("TrustClaim tag must be a string")
    if not isinstance(trust_claim.short, str):
        raise EARValidationError("TrustClaim short description must be a string")
    if not isinstance(trust_claim.long, str):
        raise EARValidationError("TrustClaim long description must be a string")


def validate_trust_vector(trust_vector: TrustVector):
    # Validates a TrustVector object
    if not isinstance(trust_vector, TrustVector):
        raise EARValidationError("Invalid TrustVector object")

    for claim in trust_vector.__dict__.values():
        if claim is not None:
            validate_trust_claim(claim)


def validate_verifier_id(verifier_id: VerifierID):
    # Validates a VerifierID object
    if not isinstance(verifier_id, VerifierID):
        raise EARValidationError("Invalid VerifierID object")
    if not verifier_id.developer or not isinstance(verifier_id.developer, str):
        raise EARValidationError("VerifierID developer must be a non-empty string")
    if not verifier_id.build or not isinstance(verifier_id.build, str):
        raise EARValidationError("VerifierID build must be a non-empty string")


def validate_ear_claims(ear_claims: EARClaims):
    # Validates an EARClaims object
    if not isinstance(ear_claims, EARClaims):
        raise EARValidationError("Invalid EARClaims object")
    if not isinstance(ear_claims.profile, str) or not ear_claims.profile:
        raise EARValidationError("EARClaims profile must be a non-empty string")
    if not isinstance(ear_claims.issued_at, int) or ear_claims.issued_at <= 0:
        raise EARValidationError("EARClaims issued_at must be a positive integer")

    validate_verifier_id(ear_claims.verifier_id)

    for submod, details in ear_claims.submods.items():
        if (
            not isinstance(details, Dict)
            or "trust_vector" not in details
            or "status" not in details
        ):
            raise EARValidationError(
                f"Submodule {submod} must contain a valid trust_vector and status"
            )

        validate_trust_vector(details["trust_vector"])


def validate_all(ear_claims: EARClaims):
    # Runs all validation checks on the provided EARClaims object
    try:
        validate_ear_claims(ear_claims)
        print("EARClaims validation successful.")
    except EARValidationError as e:
        print(f"Validation failed: {e}")
