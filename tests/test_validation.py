import pytest

from src.claims import EARClaims
from src.trust_claims import (TrustClaim, TrustworthyInstanceClaim,
                              UnsafeConfigClaim)
from src.trust_vector import TrustVector
from src.validation import (EARValidationError, validate_ear_claims,
                            validate_trust_claim, validate_trust_vector,
                            validate_verifier_id)
from src.verifier_id import VerifierID


@pytest.fixture
def valid_trust_claim():
    return TrustClaim(
        value=2,
        tag="approved_config",
        short="Approved",
        long="Configuration is approved.",
    )


@pytest.fixture
def valid_trust_vector():
    return TrustVector(
        instance_identity=TrustworthyInstanceClaim,
        configuration=UnsafeConfigClaim,
    )


@pytest.fixture
def valid_verifier_id():
    return VerifierID(developer="Acme Inc.", build="v1.0.0")


@pytest.fixture
def valid_ear_claims(valid_trust_vector, valid_verifier_id):
    return EARClaims.from_dict(
        {
            "eat_profile": "test_profile",
            "iat": 1234567890,
            "ear.verifier-id": valid_verifier_id.to_dict(),
            "submods": {
                "submod1": {
                    "trust_vector": valid_trust_vector.to_dict(),
                    "status": "affirming",
                }
            },
        }
    )


def test_validate_trust_claim(valid_trust_claim):
    # Should not raise an error
    validate_trust_claim(valid_trust_claim)


def test_validate_trust_claim_invalid():
    with pytest.raises(EARValidationError):
        validate_trust_claim(
            TrustClaim(value=200, tag="invalid", short="", long="")
        )  # Invalid value (>127)


def test_validate_trust_vector(valid_trust_vector):
    # Should not raise an error
    validate_trust_vector(valid_trust_vector)


def test_validate_trust_vector_invalid():
    with pytest.raises(EARValidationError):
        invalid_vector = TrustVector(
            configuration=TrustClaim(value=200, tag="invalid", short="", long="")
        )
        validate_trust_vector(invalid_vector)


def test_validate_verifier_id(valid_verifier_id):
    # Should not raise an error
    validate_verifier_id(valid_verifier_id)


def test_validate_verifier_id_invalid():
    with pytest.raises(EARValidationError):
        validate_verifier_id(VerifierID(developer="", build=""))  # Invalid empty fields


def test_validate_ear_claims(valid_ear_claims):
    # Should not raise an error
    validate_ear_claims(valid_ear_claims)


def test_validate_ear_claims_invalid():
    with pytest.raises(EARValidationError):
        invalid_claims = EARClaims(
            profile="", issued_at=-1, verifier_id=VerifierID(developer="", build="")
        )
        validate_ear_claims(invalid_claims)
