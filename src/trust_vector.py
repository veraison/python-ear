from dataclasses import dataclass
from typing import Optional

from src.base import BaseJCSerializable
from src.trust_claims import TrustClaim


# https://www.ietf.org/archive/id/draft-ietf-rats-ar4si-08.html#section-3.1
# TrustVector class to represent the trustworthiness vector
@dataclass
class TrustVector(BaseJCSerializable):
    instance_identity: Optional[TrustClaim] = None
    configuration: Optional[TrustClaim] = None
    executables: Optional[TrustClaim] = None
    file_system: Optional[TrustClaim] = None
    hardware: Optional[TrustClaim] = None
    runtime_opaque: Optional[TrustClaim] = None
    storage_opaque: Optional[TrustClaim] = None
    sourced_data: Optional[TrustClaim] = None

    jc_map = {
        "instance_identity": (0, "instance_identity"),
        "configuration": (1, "configuration"),
        "executables": (2, "executables"),
        "file_system": (3, "file_system"),
        "hardware": (4, "hardware"),
        "runtime_opaque": (5, "runtime_opaque"),
        "storage_opaque": (6, "storage_opaque"),
        "sourced_data": (7, "sourced_data"),
    }

    def validate(self):
        # Validates a TrustVector object

        for claim in self.__dict__.values():
            if claim is not None:
                claim.validate()
