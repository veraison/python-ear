from abc import ABC, abstractmethod
from typing import Any, Dict, Type, TypeVar, get_type_hints
import json

T = TypeVar("T", bound="BaseJCSerializable")

class BaseJCSerializable(ABC):
    jc_map: Dict[str, int]

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("to_dict must be implemented in subclasses.")

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_cbor(self) -> Dict[int, Any]:
        cbor_data = {}
        for attr, cbor_key in self.jc_map.items():
            if "." in attr:  # skiped nested keys, cuz, they will be processed when we go inside submods(not a nested key as in jc_map)
                continue
            value = getattr(self, attr, None)
            if isinstance(value, BaseJCSerializable): # trust_vector and status will be processed here
                cbor_data[cbor_key] = value.to_cbor()
            elif isinstance(value, dict): # submods will be processed here
                nested = {}
                for k, v in value.items():
                    nested[k] = self._serialize_nested_dict(attr, v)
                cbor_data[cbor_key] = nested
            elif hasattr(value, "to_dict"): # for trust_claim
                cbor_data[cbor_key] = value.to_dict()
            else:
                cbor_data[cbor_key] = value
        return cbor_data

    def _serialize_nested_dict(self, prefix: str, d: dict) -> dict:
        out = {}
        for subkey, val in d.items():
            if hasattr(val, "to_cbor"):
                out[self.jc_map[f"{prefix}.{subkey}"]] = val.to_cbor()
            elif hasattr(val, "value"): # status with trust_tier
                out[self.jc_map[f"{prefix}.{subkey}"]] = val.value
            else:
                out[self.jc_map.get(f"{prefix}.{subkey}", subkey)] = val
        return out

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        raise NotImplementedError("from_dict must be implemented in subclasses.")

    @classmethod
    def from_cbor(cls: Type[T], data: Dict[int, Any]) -> T:
        kwargs = {}
        reverse_map = {v: k for k, v in cls.jc_map.items()}
        type_hints = get_type_hints(cls)

        for key, val in data.items():
            attr = reverse_map.get(key)
            if attr is None or "." in attr:
                continue

            hint = type_hints.get(attr)

            # Handle BaseJCSerializable directly
            if isinstance(val, dict) and hasattr(hint, "from_cbor"):
                kwargs[attr] = hint.from_cbor(val)

            # Handle Dict[str, BaseJCSerializable] or Dict[str, Any] with nested mapping
            elif isinstance(val, dict) and isinstance(hint, type) and issubclass(hint, dict):
                sub_hint = None
                if hasattr(hint, "__args__") and len(hint.__args__) > 1:
                    sub_hint = hint.__args__[1]
                kwargs[attr] = {
                    k: cls._deserialize_nested_dict(attr, v, sub_hint=sub_hint)
                    for k, v in val.items()
                }

            else:
                kwargs[attr] = val

        return cls(**kwargs)

    @classmethod
    def _deserialize_nested_dict(cls, prefix: str, d: dict, sub_hint=None) -> dict:
        out = {}

        # If sub_hint isn't given, try to get it from type hints
        if sub_hint is None:
            type_hints = get_type_hints(cls)
            hint = type_hints.get(prefix)
            if hasattr(hint, '__args__') and len(hint.__args__) > 1:
                sub_hint = hint.__args__[1]

        for map_key, jc_key in cls.jc_map.items():
            if not map_key.startswith(f"{prefix}."):
                continue

            field_name = map_key.split(".")[-1]
            if jc_key in d:
                val = d[jc_key]

                # Handle BaseJCSerializable subclasses inside subdict
                if hasattr(sub_hint, 'from_cbor') and isinstance(val, dict):
                    out[field_name] = sub_hint.from_cbor(val)
                elif callable(sub_hint):
                    out[field_name] = sub_hint(val)
                else:
                    out[field_name] = val

        return out