import pytest

from src.trust_claims import TrustworthyInstanceClaim


@pytest.fixture
def trust_claim():
    # Sample TrustClaim object for testing
    return TrustworthyInstanceClaim


def test_to_dict(trust_claim):
    expected = {
        "value": 2,
        "tag": "recognized_instance",
        "short": "recognized and not compromised",
        "long": "The Attesting Environment is recognized, and the associated instance of the Attester is not known to be compromised.",  # noqa: E501
    }
    assert trust_claim.to_dict() == expected
