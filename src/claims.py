import json
from typing import Any, Dict


class EARClaims:
    def __init__(
        self,
        profile: str,
        issued_at: int,
        verifier_id: Dict[str, str],
        submods: Dict[str, Any],
    ):
        self.profile = profile
        self.issued_at = issued_at
        self.verifier_id = verifier_id
        self.submods = submods

    def to_dict(self) -> Dict[str, Any]:
        return {
            "eat_profile": self.profile,
            "iat": self.issued_at,
            "ear.verifier-id": self.verifier_id,
            "submods": self.submods,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            profile=data.get("eat_profile", ""),
            issued_at=data.get("iat", 0),
            verifier_id=data.get("ear.verifier-id", {}),
            submods=data.get("submods", {}),
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str):
        return cls.from_dict(json.loads(json_str))
