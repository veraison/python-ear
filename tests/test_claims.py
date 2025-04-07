import pytest

from src.claims import AttestationResult
from src.errors import EARValidationError
from src.trust_claims import (
    APPROVED_CONFIG_CLAIM,
    APPROVED_FILES_CLAIM,
    APPROVED_RUNTIME_CLAIM,
    ENCRYPTED_MEMORY_RUNTIME_CLAIM,
    GENUINE_HARDWARE_CLAIM,
    HW_KEYS_ENCRYPTED_SECRETS_CLAIM,
    TRUSTED_SOURCES_CLAIM,
    TRUSTWORTHY_INSTANCE_CLAIM,
)
from src.trust_tier import TRUST_TIER_AFFIRMING
from src.trust_vector import TrustVector
from src.verifier_id import VerifierID


@pytest.fixture
def sample_attestation_result():
    return AttestationResult(
        profile="test_profile",
        issued_at=1234567890,
        verifier_id=VerifierID(developer="Acme Inc.", build="v1"),
        submods={
            "submod1": {
                "trust_vector": TrustVector(
                    instance_identity=TRUSTWORTHY_INSTANCE_CLAIM,
                    configuration=APPROVED_CONFIG_CLAIM,
                    executables=APPROVED_RUNTIME_CLAIM,
                    file_system=APPROVED_FILES_CLAIM,
                    hardware=GENUINE_HARDWARE_CLAIM,
                    runtime_opaque=ENCRYPTED_MEMORY_RUNTIME_CLAIM,
                    storage_opaque=HW_KEYS_ENCRYPTED_SECRETS_CLAIM,
                    sourced_data=TRUSTED_SOURCES_CLAIM,
                ),
                "status": TRUST_TIER_AFFIRMING,
            }
        },
    )


def test_attestation_result_to_dict(sample_attestation_result):
    expected = {
        "eat_profile": "test_profile",
        "iat": 1234567890,
        "ear.verifier-id": {"developer": "Acme Inc.", "build": "v1"},
        "submods": {
            "submod1": {
                "trust_vector": {
                    "instance_identity": TRUSTWORTHY_INSTANCE_CLAIM.to_dict(),
                    "configuration": APPROVED_CONFIG_CLAIM.to_dict(),
                    "executables": APPROVED_RUNTIME_CLAIM.to_dict(),
                    "file_system": APPROVED_FILES_CLAIM.to_dict(),
                    "hardware": GENUINE_HARDWARE_CLAIM.to_dict(),
                    "runtime_opaque": ENCRYPTED_MEMORY_RUNTIME_CLAIM.to_dict(),
                    "storage_opaque": HW_KEYS_ENCRYPTED_SECRETS_CLAIM.to_dict(),
                    "sourced_data": TRUSTED_SOURCES_CLAIM.to_dict(),
                },
                "status": TRUST_TIER_AFFIRMING.value,
            }
        },
    }
    assert sample_attestation_result.to_dict() == expected


def test_attestation_result_to_json(sample_attestation_result):
    json_str = sample_attestation_result.to_json()
    parsed_claims = AttestationResult.from_json(json_str)
    assert parsed_claims.to_dict() == sample_attestation_result.to_dict()


def test_attestation_result_from_dict():
    data = {
        "eat_profile": "test_profile",
        "iat": 1234567890,
        "ear.verifier-id": {"developer": "Acme Inc.", "build": "v1"},
        "submods": {
            "submod1": {
                "trust_vector": {
                    "instance_identity": TRUSTWORTHY_INSTANCE_CLAIM.to_dict(),
                    "configuration": APPROVED_CONFIG_CLAIM.to_dict(),
                    "executables": APPROVED_RUNTIME_CLAIM.to_dict(),
                    "file_system": APPROVED_FILES_CLAIM.to_dict(),
                    "hardware": GENUINE_HARDWARE_CLAIM.to_dict(),
                    "runtime_opaque": ENCRYPTED_MEMORY_RUNTIME_CLAIM.to_dict(),
                    "storage_opaque": HW_KEYS_ENCRYPTED_SECRETS_CLAIM.to_dict(),
                    "sourced_data": TRUSTED_SOURCES_CLAIM.to_dict(),
                },
                "status": TRUST_TIER_AFFIRMING.value,
            }
        },
    }
    parsed_claims = AttestationResult.from_dict(data)
    assert parsed_claims.to_dict() == data


def test_attestation_result_to_cbor(sample_attestation_result):
    cbor_data = sample_attestation_result.to_cbor()
    expected_cbor = {
        265: "test_profile",
        6: 1234567890,
        1004: {0: "Acme Inc.", 1: "v1"},
        266: {
            "submod1": {
                1001: {
                    0: TRUSTWORTHY_INSTANCE_CLAIM.to_dict(),
                    1: APPROVED_CONFIG_CLAIM.to_dict(),
                    2: APPROVED_RUNTIME_CLAIM.to_dict(),
                    3: APPROVED_FILES_CLAIM.to_dict(),
                    4: GENUINE_HARDWARE_CLAIM.to_dict(),
                    5: ENCRYPTED_MEMORY_RUNTIME_CLAIM.to_dict(),
                    6: HW_KEYS_ENCRYPTED_SECRETS_CLAIM.to_dict(),
                    7: TRUSTED_SOURCES_CLAIM.to_dict(),
                },
                1000: TRUST_TIER_AFFIRMING.value,
            }
        },
    }
    assert cbor_data == expected_cbor


def test_attestation_result_from_cbor(sample_attestation_result):
    cbor_data = {
        265: "test_profile",
        6: 1234567890,
        1004: {0: "Acme Inc.", 1: "v1"},
        266: {
            "submod1": {
                1001: {
                    0: TRUSTWORTHY_INSTANCE_CLAIM.to_dict(),
                    1: APPROVED_CONFIG_CLAIM.to_dict(),
                    2: APPROVED_RUNTIME_CLAIM.to_dict(),
                    3: APPROVED_FILES_CLAIM.to_dict(),
                    4: GENUINE_HARDWARE_CLAIM.to_dict(),
                    5: ENCRYPTED_MEMORY_RUNTIME_CLAIM.to_dict(),
                    6: HW_KEYS_ENCRYPTED_SECRETS_CLAIM.to_dict(),
                    7: TRUSTED_SOURCES_CLAIM.to_dict(),
                },
                1000: TRUST_TIER_AFFIRMING.value,
            }
        },
    }
    import json

    parsed_claims = AttestationResult.from_cbor(cbor_data)
    assert json.dumps(parsed_claims.to_cbor(), sort_keys=True) == json.dumps(cbor_data, sort_keys=True)


def test_validate_ear_claims(sample_attestation_result):
    # Should not raise an error
    sample_attestation_result.validate()


def test_validate_ear_claims_invalid():
    with pytest.raises(EARValidationError):
        invalid_attestation_result = AttestationResult(
            profile="", issued_at=-1, verifier_id=VerifierID(developer="", build="")
        )
        invalid_attestation_result.validate()
