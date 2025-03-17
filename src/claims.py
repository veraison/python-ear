import json
from dataclasses import dataclass, field
from typing import Any, Dict

from src.base import BaseJCSerializable
from src.trust_tier import to_trust_tier
from src.trust_vector import TrustVector
from src.verifier_id import VerifierID


# https://datatracker.ietf.org/doc/draft-fv-rats-ear/
@dataclass
class AttestationResult(BaseJCSerializable):
    profile: str
    issued_at: int
    verifier_id: VerifierID
    submods: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # https://www.ietf.org/archive/id/draft-ietf-rats-eat-31.html#section-7.2.4
    JC_map = {
        "profile": 265,
        "issued_at": 6,
        "verifier_id": 1004,
        "submods": 266,
        "submod.trust_vector": 1001,
        "submod.status": 1000,
    }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "eat_profile": self.profile,
            "iat": self.issued_at,
            "ear.verifier-id": self.verifier_id.to_dict(),
            "submods": {
                key: {
                    "trust_vector": value["trust_vector"].to_dict(),
                    "status": value["status"].value,
                }
                for key, value in self.submods.items()
            },
        }

    def to_cbor(self) -> Dict[int, Any]:
        return {
            self.JC_map["profile"]: self.profile,
            self.JC_map["issued_at"]: self.issued_at,
            self.JC_map["verifier_id"]: self.verifier_id.to_cbor(),
            self.JC_map["submods"]: {
                key: {
                    self.JC_map["submod.trust_vector"]: value["trust_vector"].to_cbor(),
                    self.JC_map["submod.status"]: value["status"].value,
                }
                for key, value in self.submods.items()
            },
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            profile=data.get("eat_profile", ""),
            issued_at=data.get("iat", 0),
            verifier_id=VerifierID.from_dict(data.get("ear.verifier-id", {})),
            submods={
                key: {
                    "trust_vector": TrustVector.from_dict(value["trust_vector"]),
                    "status": to_trust_tier(value["status"]),
                }
                for key, value in data.get("submods", {}).items()
            },
        )

    @classmethod
    def from_json(cls, json_str: str):
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_cbor(cls, data: Dict[int, Any]):
        return cls(
            profile=data.get(cls.JC_map["profile"], ""),
            issued_at=data.get(cls.JC_map["issued_at"], 0),
            verifier_id=VerifierID.from_cbor(data.get(cls.JC_map["verifier_id"], {})),
            submods={
                key: {
                    "trust_vector": TrustVector.from_cbor(
                        value.get(cls.JC_map["submod.trust_vector"], {})
                    ),
                    "status": to_trust_tier(value.get(cls.JC_map["submod.status"], 0)),
                }
                for key, value in data.get(cls.JC_map["submods"], {}).items()
            },
        )
