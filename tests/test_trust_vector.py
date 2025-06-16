import json

import pytest

from src.errors import EARValidationError
from src.trust_claims import (
    APPROVED_FILES_CLAIM,
    APPROVED_RUNTIME_CLAIM,
    ENCRYPTED_MEMORY_RUNTIME_CLAIM,
    GENUINE_HARDWARE_CLAIM,
    HW_KEYS_ENCRYPTED_SECRETS_CLAIM,
    TRUSTED_SOURCES_CLAIM,
    TRUSTWORTHY_INSTANCE_CLAIM,
    UNSAFE_CONFIG_CLAIM,
    TrustClaim,
)
from src.trust_vector import TrustVector


@pytest.fixture
def sample_trust_vector():
    return TrustVector(
        instance_identity=TRUSTWORTHY_INSTANCE_CLAIM,
        configuration=UNSAFE_CONFIG_CLAIM,
        executables=APPROVED_RUNTIME_CLAIM,
        file_system=APPROVED_FILES_CLAIM,
        hardware=GENUINE_HARDWARE_CLAIM,
        runtime_opaque=ENCRYPTED_MEMORY_RUNTIME_CLAIM,
        storage_opaque=HW_KEYS_ENCRYPTED_SECRETS_CLAIM,
        sourced_data=TRUSTED_SOURCES_CLAIM,
    )


def test_trust_vector_to_dict(sample_trust_vector):
    expected = {
        "instance-identity": TRUSTWORTHY_INSTANCE_CLAIM.value,
        "configuration": UNSAFE_CONFIG_CLAIM.value,
        "executables": APPROVED_RUNTIME_CLAIM.value,
        "file-system": APPROVED_FILES_CLAIM.value,
        "hardware": GENUINE_HARDWARE_CLAIM.value,
        "runtime-opaque": ENCRYPTED_MEMORY_RUNTIME_CLAIM.value,
        "storage-opaque": HW_KEYS_ENCRYPTED_SECRETS_CLAIM.value,
        "sourced-data": TRUSTED_SOURCES_CLAIM.value,
    }
    assert sample_trust_vector.to_dict() == expected


def test_trust_vector_to_json(sample_trust_vector):
    json_str = sample_trust_vector.to_json()
    parsed_vector = TrustVector.from_dict(json.loads(json_str))
    assert parsed_vector.to_dict() == sample_trust_vector.to_dict()


def test_trust_vector_to_int_keys(sample_trust_vector):
    expected = {
        0: TRUSTWORTHY_INSTANCE_CLAIM.value,
        1: UNSAFE_CONFIG_CLAIM.value,
        2: APPROVED_RUNTIME_CLAIM.value,
        3: APPROVED_FILES_CLAIM.value,
        4: GENUINE_HARDWARE_CLAIM.value,
        5: ENCRYPTED_MEMORY_RUNTIME_CLAIM.value,
        6: HW_KEYS_ENCRYPTED_SECRETS_CLAIM.value,
        7: TRUSTED_SOURCES_CLAIM.value,
    }
    assert sample_trust_vector.to_int_keys() == expected


def test_trust_vector_from_dict():
    data = {
        "instance-identity": TRUSTWORTHY_INSTANCE_CLAIM.value,
        "configuration": UNSAFE_CONFIG_CLAIM.value,
        "executables": APPROVED_RUNTIME_CLAIM.value,
        "file-system": APPROVED_FILES_CLAIM.value,
        "hardware": GENUINE_HARDWARE_CLAIM.value,
        "runtime-opaque": ENCRYPTED_MEMORY_RUNTIME_CLAIM.value,
        "storage-opaque": HW_KEYS_ENCRYPTED_SECRETS_CLAIM.value,
        "sourced-data": TRUSTED_SOURCES_CLAIM.value,
    }
    parsed_vector = TrustVector.from_dict(data)
    assert parsed_vector.to_dict() == data


def test_trust_vector_from_int_keys():
    int_keys_data = {
        0: TRUSTWORTHY_INSTANCE_CLAIM.to_dict(),
        1: UNSAFE_CONFIG_CLAIM.to_dict(),
        2: APPROVED_RUNTIME_CLAIM.to_dict(),
        3: APPROVED_FILES_CLAIM.to_dict(),
        4: GENUINE_HARDWARE_CLAIM.to_dict(),
        5: ENCRYPTED_MEMORY_RUNTIME_CLAIM.to_dict(),
        6: HW_KEYS_ENCRYPTED_SECRETS_CLAIM.to_dict(),
        7: TRUSTED_SOURCES_CLAIM.to_dict(),
    }
    parsed_vector = TrustVector.from_int_keys(int_keys_data)
    assert (
        parsed_vector.to_dict() == TrustVector.from_int_keys(int_keys_data).to_dict()
    )  # noqa: E501


def test_validate_trust_vector(sample_trust_vector):
    # Should not raise an error
    sample_trust_vector.validate()


def test_validate_trust_vector_invalid():
    with pytest.raises(EARValidationError):
        invalid_vector = TrustVector(
            configuration=TrustClaim(value=200, tag="invalid", short="", long="")
        )
        invalid_vector.validate()
