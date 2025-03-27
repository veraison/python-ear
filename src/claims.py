import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict

from jose import jwt  # type: ignore # pylint: disable=import-error

from src.base import BaseJCSerializable
from src.errors import EARValidationError
from src.jwt_config import DEFAULT_ALGORITHM, DEFAULT_EXPIRATION_MINUTES
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
    jc_map = {
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
            self.jc_map["profile"]: self.profile,
            self.jc_map["issued_at"]: self.issued_at,
            self.jc_map["verifier_id"]: self.verifier_id.to_cbor(),
            self.jc_map["submods"]: {
                key: {
                    self.jc_map["submod.trust_vector"]: value["trust_vector"].to_cbor(),
                    self.jc_map["submod.status"]: value["status"].value,
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
            profile=data.get(cls.jc_map["profile"], ""),
            issued_at=data.get(cls.jc_map["issued_at"], 0),
            verifier_id=VerifierID.from_cbor(data.get(cls.jc_map["verifier_id"], {})),
            submods={
                key: {
                    "trust_vector": TrustVector.from_cbor(
                        value.get(cls.jc_map["submod.trust_vector"], {})
                    ),
                    "status": to_trust_tier(value.get(cls.jc_map["submod.status"], 0)),
                }
                for key, value in data.get(cls.jc_map["submods"], {}).items()
            },
        )

    def validate(self):
        # Validates an AttestationResult object
        if not isinstance(self.profile, str) or not self.profile:
            raise EARValidationError(
                "AttestationResult profile must be a non-empty string"
            )
        if not isinstance(self.issued_at, int) or self.issued_at <= 0:
            raise EARValidationError(
                "AttestationResult issued_at must be a positive integer"
            )

        self.verifier_id.validate()

        for submod, details in self.submods.items():
            if (
                not isinstance(details, Dict)
                or "trust_vector" not in details
                or "status" not in details
            ):
                raise EARValidationError(
                    f"Submodule {submod} must contain a valid trust_vector and status"
                )

            trust_vector = details["trust_vector"]
            trust_vector.validate()

    def encode_jwt(
        self,
        secret_key: str,
        algorithm: str = DEFAULT_ALGORITHM,
        expiration_minutes: int = DEFAULT_EXPIRATION_MINUTES,
    ) -> str:
        # Signs an AttestationResult object and returns a JWT
        payload = self.to_dict()
        payload["exp"] = int(
            datetime.timestamp(datetime.now() + timedelta(minutes=expiration_minutes))
        )
        return jwt.encode(payload, secret_key, algorithm=algorithm)

    @classmethod
    def decode_jwt(
        cls, token: str, secret_key: str, algorithm: str = DEFAULT_ALGORITHM
    ):
        # Verifies a JWT and returns the decoded AttestationResult object.
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            return cls.from_dict(payload)
        except Exception as exc:
            raise ValueError(f"JWT decoding failed: {exc}") from exc
