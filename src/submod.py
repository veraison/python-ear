from dataclasses import dataclass

from src.base import BaseJCSerializable
from src.trust_tier import TrustTier
from src.trust_vector import TrustVector


@dataclass
class Submod(BaseJCSerializable):
    trust_vector: TrustVector
    status: TrustTier

    jc_map = {"status": (1000, "status"), "trust_vector": (1001, "trust_vector")}
