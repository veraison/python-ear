from dataclasses import dataclass
from typing import Optional

from src.base import BaseJCSerializable, KeyMapping
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
        "instance_identity": KeyMapping(0, "instance-identity"),
        "configuration": KeyMapping(1, "configuration"),
        "executables": KeyMapping(2, "executables"),
        "file_system": KeyMapping(3, "file-system"),
        "hardware": KeyMapping(4, "hardware"),
        "runtime_opaque": KeyMapping(5, "runtime-opaque"),
        "storage_opaque": KeyMapping(6, "storage-opaque"),
        "sourced_data": KeyMapping(7, "sourced-data"),
    }

    def validate(self):
        # Validates a TrustVector object

        for claim in self.__dict__.values():
            if claim is not None:
                claim.validate()
