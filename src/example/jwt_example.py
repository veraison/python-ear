from datetime import datetime

from src.claims import AttestationResult
from src.jwt_config import generate_secret_key
from src.submod import Submod
from src.trust_claims import TRUSTWORTHY_INSTANCE_CLAIM, UNRECOGNIZED_INSTANCE_CLAIM
from src.trust_tier import TRUST_TIER_AFFIRMING, TRUST_TIER_CONTRAINDICATED
from src.trust_vector import TrustVector
from src.verifier_id import VerifierID

# import json

# Generate a secret key for signing
secret_key = generate_secret_key()

# Create an AttestationResult object
attestation_result = AttestationResult(
    profile="test_profile",
    issued_at=int(datetime.timestamp(datetime.now())),
    verifier_id=VerifierID(developer="Acme Inc.", build="v1"),
    submods={
        "submod1": Submod(
            trust_vector=TrustVector(instance_identity=UNRECOGNIZED_INSTANCE_CLAIM),
            status=TRUST_TIER_AFFIRMING,
        ),
        "submod2": Submod(
            trust_vector=TrustVector(instance_identity=TRUSTWORTHY_INSTANCE_CLAIM),
            status=TRUST_TIER_CONTRAINDICATED,
        ),
    },
)

# payload = attestation_result.encode_jwt(secret_key=secret_key)
# print(payload)

# decoded = AttestationResult.decode_jwt(token=payload, secret_key=secret_key)
# output_data = decoded.to_dict()

# with open("jwt_output.json", "w", encoding="utf-8") as f:
#     json.dump(output_data, f, indent=4)

# print("Output successfully written to output.json")
