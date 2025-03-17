import json

import pytest

from src.trust_claims import (
    APPROVED_FILES_CLAIM,
    APPROVED_RUNTIME_CLAIM,
    ENCRYPTED_MEMORY_RUNTIME_CLAIM,
    GENUINE_HARDWARE_CLAIM,
    HW_KEYS_ENCRYPTED_SECRETS_CLAIM,
    TRUSTED_SOURCES_CLAIM,
    TRUSTWORTHY_INSTANCE_CLAIM,
    UNSAFE_CONFIG_CLAIM,
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
        "instance_identity": TRUSTWORTHY_INSTANCE_CLAIM.to_dict(),
        "configuration": UNSAFE_CONFIG_CLAIM.to_dict(),
        "executables": APPROVED_RUNTIME_CLAIM.to_dict(),
        "file_system": APPROVED_FILES_CLAIM.to_dict(),
        "hardware": GENUINE_HARDWARE_CLAIM.to_dict(),
        "runtime_opaque": ENCRYPTED_MEMORY_RUNTIME_CLAIM.to_dict(),
        "storage_opaque": HW_KEYS_ENCRYPTED_SECRETS_CLAIM.to_dict(),
        "sourced_data": TRUSTED_SOURCES_CLAIM.to_dict(),
    }
    assert sample_trust_vector.to_dict() == expected


def test_trust_vector_to_json(sample_trust_vector):
    json_str = sample_trust_vector.to_json()
    parsed_vector = TrustVector.from_dict(json.loads(json_str))
    assert parsed_vector.to_dict() == sample_trust_vector.to_dict()


def test_trust_vector_to_cbor(sample_trust_vector):
    expected = {
        0: TRUSTWORTHY_INSTANCE_CLAIM.to_dict(),
        1: UNSAFE_CONFIG_CLAIM.to_dict(),
        2: APPROVED_RUNTIME_CLAIM.to_dict(),
        3: APPROVED_FILES_CLAIM.to_dict(),
        4: GENUINE_HARDWARE_CLAIM.to_dict(),
        5: ENCRYPTED_MEMORY_RUNTIME_CLAIM.to_dict(),
        6: HW_KEYS_ENCRYPTED_SECRETS_CLAIM.to_dict(),
        7: TRUSTED_SOURCES_CLAIM.to_dict(),
    }
    assert sample_trust_vector.to_cbor() == expected


def test_trust_vector_from_dict():
    data = {
        "instance_identity": TRUSTWORTHY_INSTANCE_CLAIM.to_dict(),
        "configuration": UNSAFE_CONFIG_CLAIM.to_dict(),
        "executables": APPROVED_RUNTIME_CLAIM.to_dict(),
        "file_system": APPROVED_FILES_CLAIM.to_dict(),
        "hardware": GENUINE_HARDWARE_CLAIM.to_dict(),
        "runtime_opaque": ENCRYPTED_MEMORY_RUNTIME_CLAIM.to_dict(),
        "storage_opaque": HW_KEYS_ENCRYPTED_SECRETS_CLAIM.to_dict(),
        "sourced_data": TRUSTED_SOURCES_CLAIM.to_dict(),
    }
    parsed_vector = TrustVector.from_dict(data)
    assert parsed_vector.to_dict() == data


def test_trust_vector_from_cbor():
    cbor_data = {
        0: TRUSTWORTHY_INSTANCE_CLAIM.to_dict(),
        1: UNSAFE_CONFIG_CLAIM.to_dict(),
        2: APPROVED_RUNTIME_CLAIM.to_dict(),
        3: APPROVED_FILES_CLAIM.to_dict(),
        4: GENUINE_HARDWARE_CLAIM.to_dict(),
        5: ENCRYPTED_MEMORY_RUNTIME_CLAIM.to_dict(),
        6: HW_KEYS_ENCRYPTED_SECRETS_CLAIM.to_dict(),
        7: TRUSTED_SOURCES_CLAIM.to_dict(),
    }
    parsed_vector = TrustVector.from_cbor(cbor_data)
    assert (
        parsed_vector.to_dict() == TrustVector.from_cbor(cbor_data).to_dict()
    )  # noqa: E501
