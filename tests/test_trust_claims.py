import pytest

from src.trust_claims import TRUSTWORTHY_INSTANCE_CLAIM


@pytest.fixture
def trust_claim():
    # Sample TrustClaim object for testing
    return TRUSTWORTHY_INSTANCE_CLAIM


def test_to_dict(trust_claim):
    expected = {
        "value": 2,
        "tag": "recognized_instance",
        "short": "recognized and not compromised",
        "long": "The Attesting Environment is recognized, and the associated instance of the Attester is not known to be compromised.",  # noqa: E501 # pylint: disable=line-too-long
    }
    assert trust_claim.to_dict() == expected
