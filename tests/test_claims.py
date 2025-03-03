from src.claims import EARClaims


def test_ear_claims():
    claims = EARClaims(
        "test_profile",
        1234567890,
        {"build": "v1"},
        {"submods1": {"status": "affirming"}},
    )
    json_str = claims.to_json()
    parsed_claims = EARClaims.from_json(json_str)
    assert parsed_claims.to_dict() == claims.to_dict()
