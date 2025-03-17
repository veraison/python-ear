from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from src.base import BaseJCSerializable
from src.trust_claims import TrustClaim


# https://www.ietf.org/archive/id/draft-ietf-rats-ar4si-08.html#section-3.1
# TrustVector class to represent the trustworthiness vector
@dataclass
class TrustVector(BaseJCSerializable):
    instance_identity: Optional[TrustClaim] = None
    configuration: Optional[TrustClaim] = None
    executables: Optional[TrustClaim] = None
    file_system: Optional[TrustClaim] = None
    hardware: Optional[TrustClaim] = None
    runtime_opaque: Optional[TrustClaim] = None
    storage_opaque: Optional[TrustClaim] = None
    sourced_data: Optional[TrustClaim] = None

    JC_map = {
        "instance_identity": 0,
        "configuration": 1,
        "executables": 2,
        "file_system": 3,
        "hardware": 4,
        "runtime_opaque": 5,
        "storage_opaque": 6,
        "sourced_data": 7,
    }

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_cbor(self) -> Dict[int, Dict[str, Any]]:
        return {
            index: getattr(self, field).to_dict()
            for field, index in self.JC_map.items()
            if getattr(self, field)
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        kwargs = {
            field: TrustClaim(**data[field]) if data.get(field) else None
            for field in cls.JC_map
        }
        return cls(**kwargs)

    @classmethod
    def from_cbor(cls, data: Dict[int, Dict[str, Any]]):
        reverse_map = {v: k for k, v in cls.JC_map.items()}
        kwargs = {
            reverse_map[index]: TrustClaim(**value)
            for index, value in data.items()
            if index in reverse_map
        }
        return cls(**kwargs)
