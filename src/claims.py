import json
from dataclasses import dataclass, field
from typing import Any, Dict

from src.trust_vector import TrustVector
from src.verifier_id import VerifierID


# Represents the EAR Claims set that will be populated
@dataclass
class EARClaims:
    profile: str
    issued_at: int
    verifier_id: VerifierID
    submods: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Returns a python dictionary that will be used for serializing to JWT
    def to_dict(self) -> Dict[str, Any]:
        return {
            "eat_profile": self.profile,
            "iat": self.issued_at,
            "ear.verifier-id": self.verifier_id.to_dict(),
            "submods": {
                key: {
                    "trust_vector": value["trust_vector"].to_dict(),
                    "status": value["status"],
                }
                for key, value in self.submods.items()
            },
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            profile=data.get("eat_profile", ""),
            issued_at=data.get("iat", 0),
            verifier_id=VerifierID.from_dict(data.get("ear.verifier-id", {})),
            submods={
                key: {
                    "trust_vector": TrustVector.from_dict(value["trust_vector"]),  # noqa: E501
                    "status": value["status"],
                }
                for key, value in data.get("submods", {}).items()
            },
        )

    @classmethod
    def from_json(cls, json_str: str):
        return cls.from_dict(json.loads(json_str))
