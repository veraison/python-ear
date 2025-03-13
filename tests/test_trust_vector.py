import json

import pytest

from src.trust_claims import (
    ApprovedFilesClaim,
    ApprovedRuntimeClaim,
    EncryptedMemoryRuntimeClaim,
    GenuineHardwareClaim,
    HwKeysEncryptedSecretsClaim,
    TrustedSourcesClaim,
    TrustworthyInstanceClaim,
    UnsafeConfigClaim,
)
from src.trust_vector import TrustVector


@pytest.fixture
def sample_trust_vector():
    return TrustVector(
        instance_identity=TrustworthyInstanceClaim,
        configuration=UnsafeConfigClaim,
        executables=ApprovedRuntimeClaim,
        file_system=ApprovedFilesClaim,
        hardware=GenuineHardwareClaim,
        runtime_opaque=EncryptedMemoryRuntimeClaim,
        storage_opaque=HwKeysEncryptedSecretsClaim,
        sourced_data=TrustedSourcesClaim,
    )


def test_trust_vector_to_dict(sample_trust_vector):
    expected = {
        "instance_identity": TrustworthyInstanceClaim.to_dict(),
        "configuration": UnsafeConfigClaim.to_dict(),
        "executables": ApprovedRuntimeClaim.to_dict(),
        "file_system": ApprovedFilesClaim.to_dict(),
        "hardware": GenuineHardwareClaim.to_dict(),
        "runtime_opaque": EncryptedMemoryRuntimeClaim.to_dict(),
        "storage_opaque": HwKeysEncryptedSecretsClaim.to_dict(),
        "sourced_data": TrustedSourcesClaim.to_dict(),
    }
    assert sample_trust_vector.to_dict() == expected


def test_trust_vector_to_json(sample_trust_vector):
    json_str = sample_trust_vector.to_json()
    parsed_vector = TrustVector.from_dict(json.loads(json_str))
    assert parsed_vector.to_dict() == sample_trust_vector.to_dict()


def test_trust_vector_to_cbor(sample_trust_vector):
    expected = {
        0: TrustworthyInstanceClaim.to_dict(),
        1: UnsafeConfigClaim.to_dict(),
        2: ApprovedRuntimeClaim.to_dict(),
        3: ApprovedFilesClaim.to_dict(),
        4: GenuineHardwareClaim.to_dict(),
        5: EncryptedMemoryRuntimeClaim.to_dict(),
        6: HwKeysEncryptedSecretsClaim.to_dict(),
        7: TrustedSourcesClaim.to_dict(),
    }
    assert sample_trust_vector.to_cbor() == expected


def test_trust_vector_from_dict():
    data = {
        "instance_identity": TrustworthyInstanceClaim.to_dict(),
        "configuration": UnsafeConfigClaim.to_dict(),
        "executables": ApprovedRuntimeClaim.to_dict(),
        "file_system": ApprovedFilesClaim.to_dict(),
        "hardware": GenuineHardwareClaim.to_dict(),
        "runtime_opaque": EncryptedMemoryRuntimeClaim.to_dict(),
        "storage_opaque": HwKeysEncryptedSecretsClaim.to_dict(),
        "sourced_data": TrustedSourcesClaim.to_dict(),
    }
    parsed_vector = TrustVector.from_dict(data)
    assert parsed_vector.to_dict() == data


def test_trust_vector_from_cbor():
    cbor_data = {
        0: TrustworthyInstanceClaim.to_dict(),
        1: UnsafeConfigClaim.to_dict(),
        2: ApprovedRuntimeClaim.to_dict(),
        3: ApprovedFilesClaim.to_dict(),
        4: GenuineHardwareClaim.to_dict(),
        5: EncryptedMemoryRuntimeClaim.to_dict(),
        6: HwKeysEncryptedSecretsClaim.to_dict(),
        7: TrustedSourcesClaim.to_dict(),
    }
    parsed_vector = TrustVector.from_cbor(cbor_data)
    assert parsed_vector.to_dict() == TrustVector.from_cbor(cbor_data).to_dict()  # noqa: E501
