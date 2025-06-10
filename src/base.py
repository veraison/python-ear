import json
from abc import ABC
from collections import namedtuple
from typing import Any, ClassVar, Dict, Tuple, Type, TypeVar, Union, get_args

T = TypeVar("T", bound="BaseJCSerializable")

KeyMapping = namedtuple("KeyMapping", ["int_key", "str_key"])


def to_data(value: Any, keys_as_int=False) -> Any:
    if hasattr(value, "to_data"):
        return value.to_data(keys_as_int)
    if hasattr(value, "items"):  # dict-like
        return {
            to_data(k, keys_as_int): to_data(v, keys_as_int) for k, v in value.items()
        }
    if hasattr(value, "__iter__") and not isinstance(value, str):  # list-like
        return [to_data(v, keys_as_int) for v in value]

    if hasattr(
        value, "value"
    ):  # custom classes that have value attr but don't have 'to_data'
        return value.value  # type: ignore[attr-defined]
    # scalar and no to_data(), so assume serializable as-is
    return value


class BaseJCSerializable(ABC):
    jc_map: ClassVar[Dict[str, Tuple[int, str]]]

    def to_data(self, keys_as_int=False) -> Dict[Union[str, int], Any]:
        return {
            (int_key if keys_as_int else str_key): to_data(
                getattr(self, attr), keys_as_int
            )
            for attr, (int_key, str_key) in self.jc_map.items()
        }

    @classmethod
    def from_data(cls: Type[T], data: dict, keys_as_int=False) -> T:
        key_attr = "int_key" if keys_as_int else "str_key"
        init_kwargs = {}
        reverse_map = {
            getattr(mapping, key_attr): attr for attr, mapping in cls.jc_map.items()
        }

        for key, value in data.items():
            if key not in reverse_map:
                continue

            attr = reverse_map[key]
            field_type = getattr(cls, "__annotations__", {}).get(attr)
            if field_type is None:
                continue

            args = get_args(field_type)

            if hasattr(field_type, "from_data"):
                # Direct object
                init_kwargs[attr] = field_type.from_data(value, keys_as_int=keys_as_int)

            elif hasattr(field_type, "items") and hasattr(args[1], "from_data"):
                # Dict[str | int, CustomClass]
                init_kwargs[attr] = {
                    k: args[1].from_data(v, keys_as_int=keys_as_int)
                    for k, v in value.items()
                }

            elif args:
                # custom classes that dont have 'from_data'
                init_kwargs[attr] = args[0](value)

            else:
                init_kwargs[attr] = field_type(value)

        return cls(**init_kwargs)

    def to_dict(self) -> Dict[str, Any]:
        # default str_keys
        return self.to_data()  # type: ignore[return-value] # pyright: ignore[reportGeneralTypeIssues] # noqa: E501 # pylint: disable=line-too-long

    def to_int_keys(self) -> Dict[Union[str, int], Any]:
        return self.to_data(keys_as_int=True)

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        return cls.from_data(data)

    @classmethod
    def from_int_keys(cls: Type[T], data: Dict[int, Any]) -> T:
        return cls.from_data(data, keys_as_int=True)

    @classmethod
    def from_json(cls, json_str: str):
        return cls.from_dict(json.loads(json_str))

    def to_json(self):
        return json.dumps(self.to_data())
