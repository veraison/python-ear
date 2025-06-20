import pytest

from src.errors import EARValidationError
from src.trust_claims import TRUSTWORTHY_INSTANCE_CLAIM, TrustClaim


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


def test_validate_trust_claim_valid(trust_claim):
    # Should not raise an error
    trust_claim.validate()


def test_validate_trust_claim_invalid():
    with pytest.raises(EARValidationError):
        invalid_trust_claim = TrustClaim(value=200, tag="invalid", short="", long="")
        invalid_trust_claim.validate()
