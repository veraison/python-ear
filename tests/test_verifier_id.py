import json

import pytest

from src.errors import EARValidationError
from src.verifier_id import VerifierID


@pytest.fixture
def verifier():
    # Sample VerifierID object for testing
    return VerifierID(developer="Acme Inc.", build="v1.0.0")


def test_to_dict(verifier):  # pylint: disable=redefined-outer-name
    expected = {"developer": "Acme Inc.", "build": "v1.0.0"}
    assert verifier.to_dict() == expected


def test_to_json(verifier):  # pylint: disable=redefined-outer-name
    expected = json.dumps({"developer": "Acme Inc.", "build": "v1.0.0"})
    assert verifier.to_json() == expected


def test_to_cbor(verifier):  # pylint: disable=redefined-outer-name
    expected = {0: "Acme Inc.", 1: "v1.0.0"}
    assert verifier.to_cbor() == expected


def test_from_dict():
    data = {"developer": "Acme Inc.", "build": "v1.0.0"}
    sample_verifier = VerifierID.from_dict(data)
    assert sample_verifier.developer == "Acme Inc."
    assert sample_verifier.build == "v1.0.0"


def test_from_cbor():
    cbor_data = {0: "Acme Inc.", 1: "v1.0.0"}
    sample_verifier = VerifierID.from_cbor(cbor_data)
    assert sample_verifier.developer == "Acme Inc."
    assert sample_verifier.build == "v1.0.0"


def test_validate_verifier_id(verifier):
    # Should not raise an error
    verifier.validate()


def test_validate_verifier_id_invalid():
    with pytest.raises(EARValidationError):
        invalid_verifier_id = VerifierID(developer="", build="")  # Invalid empty fields
        invalid_verifier_id.validate()
