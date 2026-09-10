"""Password hashing with stdlib PBKDF2 — portable, no extra crypto package."""

from __future__ import annotations

import hashlib
import hmac
import secrets

_ROUNDS = 100_000
DEMO_PASSWORD = "sample"


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("ascii"), _ROUNDS
    )
    return f"pbkdf2_sha256${_ROUNDS}${salt}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        scheme, rounds_s, salt, digest_hex = stored.split("$")
        if scheme != "pbkdf2_sha256":
            return False
        rounds = int(rounds_s)
    except ValueError:
        return False
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("ascii"), rounds
    )
    return hmac.compare_digest(digest.hex(), digest_hex)
