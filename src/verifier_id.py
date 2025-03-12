from dataclasses import asdict, dataclass
from typing import Any, Dict

from src.base import BaseJCSerializable


@dataclass
class VerifierID(BaseJCSerializable):
    developer: str
    build: str
    # https://www.ietf.org/archive/id/draft-ietf-rats-ar4si-08.html#section-3.3
    JC_map = {
        "developer": 0,  # JC<"developer", 0>
        "build": 1,  # JC<"build", 1>
    }

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    # Convert to a dict with integer keys (for CBOR)
    def to_cbor(self) -> Dict[int, str]:
        return {
            index: getattr(self, field) for field, index in self.JC_map.items()
        }  # noqa: E501

    # Create an instance from a dict with string keys
    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        return cls(**data)

    # Create an instance from a CBOR-like dict (integer keys)
    @classmethod
    def from_cbor(cls, data: Dict[int, str]):
        reverse_map = {v: k for k, v in cls.JC_map.items()}
        kwargs = {reverse_map[index]: value for index, value in data.items()}
        return cls(**kwargs)
