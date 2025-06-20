from dataclasses import dataclass

from src.base import BaseJCSerializable, KeyMapping
from src.trust_tier import TrustTier
from src.trust_vector import TrustVector


@dataclass
class Submod(BaseJCSerializable):
    trust_vector: TrustVector
    status: TrustTier

    jc_map = {
        "status": KeyMapping(1000, "ear.status"),
        "trust_vector": KeyMapping(1001, "ear.trustworthiness-vector"),
    }
