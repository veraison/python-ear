import json

import pytest

from src.claims import AttestationResult
from src.errors import EARValidationError
from src.submod import Submod
from src.trust_claims import (
    APPROVED_CONFIG_CLAIM,
    APPROVED_FILES_CLAIM,
    APPROVED_RUNTIME_CLAIM,
    ENCRYPTED_MEMORY_RUNTIME_CLAIM,
    GENUINE_HARDWARE_CLAIM,
    HW_KEYS_ENCRYPTED_SECRETS_CLAIM,
    TRUSTED_SOURCES_CLAIM,
    TRUSTWORTHY_INSTANCE_CLAIM,
    TrustClaim,
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
            "submod1": Submod(
                trust_vector=TrustVector(
                    instance_identity=TrustClaim(2),
                    configuration=TrustClaim(2),
                    executables=TrustClaim(2),
                    file_system=TrustClaim(2),
                    hardware=TrustClaim(2),
                    runtime_opaque=TrustClaim(2),
                    storage_opaque=TrustClaim(2),
                    sourced_data=TrustClaim(2),
                ),
                status=TRUST_TIER_AFFIRMING,
            ),
        },
    )


def test_attestation_result_to_dict(sample_attestation_result):
    expected = {
        "eat_profile": "test_profile",
        "iat": 1234567890,
        "ear.verifier-id": {"developer": "Acme Inc.", "build": "v1"},
        "submods": {
            "submod1": {
                "ear.trustworthiness-vector": {
                    "instance-identity": TRUSTWORTHY_INSTANCE_CLAIM.value,
                    "configuration": APPROVED_CONFIG_CLAIM.value,
                    "executables": APPROVED_RUNTIME_CLAIM.value,
                    "file-system": APPROVED_FILES_CLAIM.value,
                    "hardware": GENUINE_HARDWARE_CLAIM.value,
                    "runtime-opaque": ENCRYPTED_MEMORY_RUNTIME_CLAIM.value,
                    "storage-opaque": HW_KEYS_ENCRYPTED_SECRETS_CLAIM.value,
                    "sourced-data": TRUSTED_SOURCES_CLAIM.value,
                },
                "ear.status": TRUST_TIER_AFFIRMING.value,
            }
        },
    }
    assert sample_attestation_result.to_dict() == expected


def test_attestation_result_to_json(sample_attestation_result):
    json_str = sample_attestation_result.to_json()
    parsed_claims = AttestationResult.from_json(json_str=json_str)
    assert parsed_claims.to_dict() == sample_attestation_result.to_dict()


def test_attestation_result_from_dict():
    data = {
        "eat_profile": "test_profile",
        "iat": 1234567890,
        "ear.verifier-id": {"developer": "Acme Inc.", "build": "v1"},
        "submods": {
            "submod1": {
                "ear.trustworthiness-vector": {
                    "instance-identity": TRUSTWORTHY_INSTANCE_CLAIM.value,
                    "configuration": APPROVED_CONFIG_CLAIM.value,
                    "executables": APPROVED_RUNTIME_CLAIM.value,
                    "file-system": APPROVED_FILES_CLAIM.value,
                    "hardware": GENUINE_HARDWARE_CLAIM.value,
                    "runtime-opaque": ENCRYPTED_MEMORY_RUNTIME_CLAIM.value,
                    "storage-opaque": HW_KEYS_ENCRYPTED_SECRETS_CLAIM.value,
                    "sourced-data": TRUSTED_SOURCES_CLAIM.value,
                },
                "ear.status": TRUST_TIER_AFFIRMING.value,
            }
        },
    }
    parsed_claims = AttestationResult.from_dict(data)
    assert parsed_claims.to_dict() == data


def test_attestation_result_to_int_keys(sample_attestation_result):
    int_keys_data = sample_attestation_result.to_int_keys()
    expected_int_keys = {
        265: "test_profile",
        6: 1234567890,
        1004: {0: "Acme Inc.", 1: "v1"},
        266: {
            "submod1": {
                1001: {
                    0: TRUSTWORTHY_INSTANCE_CLAIM.value,
                    1: APPROVED_CONFIG_CLAIM.value,
                    2: APPROVED_RUNTIME_CLAIM.value,
                    3: APPROVED_FILES_CLAIM.value,
                    4: GENUINE_HARDWARE_CLAIM.value,
                    5: ENCRYPTED_MEMORY_RUNTIME_CLAIM.value,
                    6: HW_KEYS_ENCRYPTED_SECRETS_CLAIM.value,
                    7: TRUSTED_SOURCES_CLAIM.value,
                },
                1000: TRUST_TIER_AFFIRMING.value,
            }
        },
    }
    assert int_keys_data == expected_int_keys


def test_attestation_result_from_int_keys():
    int_keys_data = {
        265: "test_profile",
        6: 1234567890,
        1004: {0: "Acme Inc.", 1: "v1"},
        266: {
            "submod1": {
                1001: {
                    0: TRUSTWORTHY_INSTANCE_CLAIM.value,
                    1: APPROVED_CONFIG_CLAIM.value,
                    2: APPROVED_RUNTIME_CLAIM.value,
                    3: APPROVED_FILES_CLAIM.value,
                    4: GENUINE_HARDWARE_CLAIM.value,
                    5: ENCRYPTED_MEMORY_RUNTIME_CLAIM.value,
                    6: HW_KEYS_ENCRYPTED_SECRETS_CLAIM.value,
                    7: TRUSTED_SOURCES_CLAIM.value,
                },
                1000: TRUST_TIER_AFFIRMING.value,
            }
        },
    }

    parsed_claims = AttestationResult.from_int_keys(int_keys_data)
    assert json.dumps(parsed_claims.to_int_keys(), sort_keys=True) == json.dumps(
        int_keys_data, sort_keys=True
    )


def test_validate_ear_claims(sample_attestation_result):
    # Should not raise an error
    sample_attestation_result.validate()


def test_validate_ear_claims_invalid():
    with pytest.raises(EARValidationError):
        invalid_attestation_result = AttestationResult(
            profile="", issued_at=-1, verifier_id=VerifierID(developer="", build="")
        )
        invalid_attestation_result.validate()
