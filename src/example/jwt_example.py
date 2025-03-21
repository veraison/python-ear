from datetime import datetime

from src.claims import AttestationResult
from src.jwt_handler import decode_ear_claims, generate_secret_key, sign_ear_claims
from src.trust_claims import TRUSTWORTHY_INSTANCE_CLAIM, UNRECOGNIZED_INSTANCE_CLAIM
from src.trust_tier import TRUST_TIER_AFFIRMING, TRUST_TIER_CONTRAINDICATED
from src.trust_vector import TrustVector
from src.verifier_id import VerifierID

# Generate a secret key for signing
secret_key = generate_secret_key()

# Create an AttestationResult object
attestation_result = AttestationResult(
    profile="test_profile",
    issued_at=int(datetime.timestamp(datetime.now())),
    verifier_id=VerifierID(developer="Acme Inc.", build="v1"),
    submods={
        "submod1": {
            "trust_vector": TrustVector(instance_identity=UNRECOGNIZED_INSTANCE_CLAIM),
            "status": TRUST_TIER_AFFIRMING,
        },
        "submod2": {
            "trust_vector": TrustVector(instance_identity=TRUSTWORTHY_INSTANCE_CLAIM),
            "status": TRUST_TIER_CONTRAINDICATED,
        },
    },
)

signed_jwt_token = sign_ear_claims(attestation_result, secret_key)

# Prepare data to be written to a JSON file
output_data = {
    "generated_secret_key": secret_key,
    "original_attestation_result_json": attestation_result.to_dict(),
    "original_attestation_result_cbor": attestation_result.to_cbor(),
    "signed_jwt_token": signed_jwt_token,
}

# Decode the JWT and add decoded claims
decoded_claims = decode_ear_claims(signed_jwt_token, secret_key)
output_data["decoded_attestation_result"] = decoded_claims.to_dict()

# Save to output.json
"""
with open("jwt_output.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=4)

print("Output successfully written to output.json")
"""
