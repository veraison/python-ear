from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict

from jose import jwt  # type: ignore # pylint: disable=import-error

from src.base import BaseJCSerializable, KeyMapping
from src.errors import EARValidationError
from src.jwt_config import DEFAULT_ALGORITHM, DEFAULT_EXPIRATION_MINUTES
from src.submod import Submod
from src.verifier_id import VerifierID


# https://datatracker.ietf.org/doc/draft-fv-rats-ear/
@dataclass
class AttestationResult(BaseJCSerializable):
    profile: str
    issued_at: int
    verifier_id: VerifierID
    submods: Dict[str, Submod] = field(default_factory=dict)

    # https://www.ietf.org/archive/id/draft-ietf-rats-eat-31.html#section-7.2.4
    jc_map = {
        "profile": KeyMapping(265, "profile"),
        "issued_at": KeyMapping(6, "issued_at"),
        "verifier_id": KeyMapping(1004, "verifier_id"),
        "submods": KeyMapping(266, "submods"),
    }

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
            if not isinstance(details, Submod):
                raise EARValidationError(
                    f"Submodule {submod} must contain a valid trust_vector and status"
                )

            trust_vector = details.trust_vector
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
        return jwt.encode(
            payload, secret_key, algorithm=algorithm
        )  # pyright: ignore[reportGeneralTypeIssues]

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
