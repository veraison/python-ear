import pytest

from src.trust_tier import (TrustTierAffirming, TrustTierContraindicated,
                            TrustTierNone, TrustTierWarning, to_trust_tier)


def test_to_trust_tier_valid_int():
    assert to_trust_tier(0) == TrustTierNone
    assert to_trust_tier(2) == TrustTierAffirming
    assert to_trust_tier(32) == TrustTierWarning
    assert to_trust_tier(96) == TrustTierContraindicated


def test_to_trust_tier_valid_str():
    assert to_trust_tier("none") == TrustTierNone
    assert to_trust_tier("affirming") == TrustTierAffirming
    assert to_trust_tier("warning") == TrustTierWarning
    assert to_trust_tier("contraindicated") == TrustTierContraindicated


def test_to_trust_tier_invalid_int():
    assert to_trust_tier(100) == TrustTierNone  # Default fallback


def test_to_trust_tier_invalid_str():
    assert to_trust_tier("invalid_string") == TrustTierNone  # Default fallback


def test_to_trust_tier_invalid_type():
    with pytest.raises(ValueError):
        to_trust_tier([1, 2, 3])

    with pytest.raises(ValueError):
        to_trust_tier({"tier": "affirming"})
