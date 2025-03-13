import pytest

from src.claims import EARClaims
from src.trust_claims import (
    ApprovedConfigClaim,
    ApprovedFilesClaim,
    ApprovedRuntimeClaim,
    EncryptedMemoryRuntimeClaim,
    GenuineHardwareClaim,
    HwKeysEncryptedSecretsClaim,
    TrustedSourcesClaim,
    TrustworthyInstanceClaim,
)
from src.trust_vector import TrustVector
from src.verifier_id import VerifierID


@pytest.fixture
def sample_ear_claims():
    return EARClaims(
        profile="test_profile",
        issued_at=1234567890,
        verifier_id=VerifierID(developer="Acme Inc.", build="v1"),
        submods={
            "submod1": {
                "trust_vector": TrustVector(
                    instance_identity=TrustworthyInstanceClaim,
                    configuration=ApprovedConfigClaim,
                    executables=ApprovedRuntimeClaim,
                    file_system=ApprovedFilesClaim,
                    hardware=GenuineHardwareClaim,
                    runtime_opaque=EncryptedMemoryRuntimeClaim,
                    storage_opaque=HwKeysEncryptedSecretsClaim,
                    sourced_data=TrustedSourcesClaim,
                ),
                "status": "affirming",
            }
        },
    )


def test_ear_claims_to_dict(sample_ear_claims):
    expected = {
        "eat_profile": "test_profile",
        "iat": 1234567890,
        "ear.verifier-id": {"developer": "Acme Inc.", "build": "v1"},
        "submods": {
            "submod1": {
                "trust_vector": {
                    "instance_identity": TrustworthyInstanceClaim.to_dict(),
                    "configuration": ApprovedConfigClaim.to_dict(),
                    "executables": ApprovedRuntimeClaim.to_dict(),
                    "file_system": ApprovedFilesClaim.to_dict(),
                    "hardware": GenuineHardwareClaim.to_dict(),
                    "runtime_opaque": EncryptedMemoryRuntimeClaim.to_dict(),
                    "storage_opaque": HwKeysEncryptedSecretsClaim.to_dict(),
                    "sourced_data": TrustedSourcesClaim.to_dict(),
                },
                "status": "affirming",
            }
        },
    }
    assert sample_ear_claims.to_dict() == expected


def test_ear_claims_to_json(sample_ear_claims):
    json_str = sample_ear_claims.to_json()
    parsed_claims = EARClaims.from_json(json_str)
    assert parsed_claims.to_dict() == sample_ear_claims.to_dict()


def test_ear_claims_from_dict():
    data = {
        "eat_profile": "test_profile",
        "iat": 1234567890,
        "ear.verifier-id": {"developer": "Acme Inc.", "build": "v1"},
        "submods": {
            "submod1": {
                "trust_vector": {
                    "instance_identity": TrustworthyInstanceClaim.to_dict(),
                    "configuration": ApprovedConfigClaim.to_dict(),
                    "executables": ApprovedRuntimeClaim.to_dict(),
                    "file_system": ApprovedFilesClaim.to_dict(),
                    "hardware": GenuineHardwareClaim.to_dict(),
                    "runtime_opaque": EncryptedMemoryRuntimeClaim.to_dict(),
                    "storage_opaque": HwKeysEncryptedSecretsClaim.to_dict(),
                    "sourced_data": TrustedSourcesClaim.to_dict(),
                },
                "status": "affirming",
            }
        },
    }
    parsed_claims = EARClaims.from_dict(data)
    assert parsed_claims.to_dict() == data
