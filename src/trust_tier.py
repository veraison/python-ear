from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class TrustTier:
    value: int


def to_trust_tier(value: Any) -> TrustTier:
    # Converts an integer or string to a TrustTier instance, defaulting to TrustTierNone on failure
    if isinstance(value, int):
        return IntToTrustTier.get(value, TrustTierNone)
    if isinstance(value, str):
        return StringToTrustTier.get(value, TrustTierNone)
    raise ValueError(f"Cannot convert {value} (type {type(value)}) to TrustTier")


# Defining trust tiers
TrustTierNone = TrustTier(0)
TrustTierAffirming = TrustTier(2)
TrustTierWarning = TrustTier(32)
TrustTierContraindicated = TrustTier(96)

# Mapping from TrustTier to string representation
TrustTierToString: Dict[TrustTier, str] = {
    TrustTierNone: "none",
    TrustTierAffirming: "affirming",
    TrustTierWarning: "warning",
    TrustTierContraindicated: "contraindicated",
}

# Reverse mapping from string to TrustTier
StringToTrustTier: Dict[str, TrustTier] = {v: k for k, v in TrustTierToString.items()}

# Mapping from integer value to TrustTier
IntToTrustTier: Dict[int, TrustTier] = {
    TrustTierNone.value: TrustTierNone,
    TrustTierAffirming.value: TrustTierAffirming,
    TrustTierWarning.value: TrustTierWarning,
    TrustTierContraindicated.value: TrustTierContraindicated,
}
