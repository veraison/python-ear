from dataclasses import dataclass
from typing import Any, Dict


# https://www.ietf.org/archive/id/draft-ietf-rats-ar4si-08.html#section-3.2
@dataclass(frozen=True)
class TrustTier:
    value: int


def to_trust_tier(value: Any) -> TrustTier:
    # Converts an integer or string to a TrustTier instance,
    # defaulting to TrustTierNone on failure
    if isinstance(value, int):
        return INT_TO_TRUST_TIER.get(value, TRUST_TIER_NONE)
    if isinstance(value, str):
        return STRING_TO_TRUST_TIER.get(value, TRUST_TIER_NONE)
    raise ValueError(f"Cannot convert {value} (type {type(value)}) to TrustTier")


# Defining trust tiers
TRUST_TIER_NONE: TrustTier = TrustTier(0)
TRUST_TIER_AFFIRMING: TrustTier = TrustTier(2)
TRUST_TIER_WARNING: TrustTier = TrustTier(32)
TRUST_TIER_CONTRAINDICATED: TrustTier = TrustTier(96)

# Mapping from TrustTier to string representation
TRUST_TIER_TO_STRING: Dict[TrustTier, str] = {
    TRUST_TIER_NONE: "none",
    TRUST_TIER_AFFIRMING: "affirming",
    TRUST_TIER_WARNING: "warning",
    TRUST_TIER_CONTRAINDICATED: "contraindicated",
}

# Reverse mapping from string to TrustTier
STRING_TO_TRUST_TIER: Dict[str, TrustTier] = {
    v: k for k, v in TRUST_TIER_TO_STRING.items()
}

# Mapping from integer value to TrustTier
INT_TO_TRUST_TIER: Dict[int, TrustTier] = {
    TRUST_TIER_NONE.value: TRUST_TIER_NONE,
    TRUST_TIER_AFFIRMING.value: TRUST_TIER_AFFIRMING,
    TRUST_TIER_WARNING.value: TRUST_TIER_WARNING,
    TRUST_TIER_CONTRAINDICATED.value: TRUST_TIER_CONTRAINDICATED,
}
