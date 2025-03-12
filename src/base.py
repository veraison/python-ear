import json
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseJCSerializable(ABC):
    JC_map: Dict[str, int]

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @abstractmethod
    def to_cbor(self) -> Dict[int, Any]:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]):
        pass

    @classmethod
    @abstractmethod
    def from_cbor(cls, data: Dict[int, Any]):
        pass
