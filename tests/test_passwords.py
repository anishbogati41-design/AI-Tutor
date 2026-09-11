from backend.auth.passwords import hash_password, verify_password


def test_password_hash_round_trip() -> None:
    encoded = hash_password("correct horse battery staple")

    assert encoded != "correct horse battery staple"
    assert verify_password("correct horse battery staple", encoded) is True
    assert verify_password("wrong password", encoded) is False


def test_password_hashes_use_unique_salts() -> None:
    first = hash_password("same password")
    second = hash_password("same password")

    assert first != second


def test_password_verification_rejects_unknown_or_modified_formats() -> None:
    encoded = hash_password("valid password")
    modified_cost = encoded.replace("scrypt$16384", "scrypt$32768")

    assert verify_password("valid password", "not-a-password-hash") is False
    assert verify_password("valid password", modified_cost) is False
