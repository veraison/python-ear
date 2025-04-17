from dataclasses import dataclass

from src.base import BaseJCSerializable
from src.errors import EARValidationError


# https://www.ietf.org/archive/id/draft-ietf-rats-ar4si-08.html#section-3.3
@dataclass
class VerifierID(BaseJCSerializable):
    developer: str
    build: str
    jc_map = {
        "developer": (0, "developer"),  # JC<"developer", 0>
        "build": (1, "build"),  # JC<"build", 1>
    }

    def validate(self):
        # Validates a VerifierID object
        if not self.developer or not isinstance(self.developer, str):
            raise EARValidationError("VerifierID developer must be a non-empty string")
        if not self.build or not isinstance(self.build, str):
            raise EARValidationError("VerifierID build must be a non-empty string")
