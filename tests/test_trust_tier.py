import pytest

from src.trust_tier import (
    TRUST_TIER_AFFIRMING,
    TRUST_TIER_CONTRAINDICATED,
    TRUST_TIER_NONE,
    TRUST_TIER_WARNING,
    to_trust_tier,
)


def test_to_trust_tier_valid_int():
    assert to_trust_tier(0) == TRUST_TIER_NONE
    assert to_trust_tier(2) == TRUST_TIER_AFFIRMING
    assert to_trust_tier(32) == TRUST_TIER_WARNING
    assert to_trust_tier(96) == TRUST_TIER_CONTRAINDICATED


def test_to_trust_tier_valid_str():
    assert to_trust_tier("none") == TRUST_TIER_NONE
    assert to_trust_tier("affirming") == TRUST_TIER_AFFIRMING
    assert to_trust_tier("warning") == TRUST_TIER_WARNING
    assert to_trust_tier("contraindicated") == TRUST_TIER_CONTRAINDICATED


def test_to_trust_tier_invalid_int():
    assert to_trust_tier(100) == TRUST_TIER_NONE  # Default fallback


def test_to_trust_tier_invalid_str():
    assert to_trust_tier("invalid_string") == TRUST_TIER_NONE  # Default fallback


def test_to_trust_tier_invalid_type():
    with pytest.raises(ValueError):
        to_trust_tier([1, 2, 3])

    with pytest.raises(ValueError):
        to_trust_tier({"tier": "affirming"})
