"""Password hashing and role priority."""

from deskflow.db.identity import primary_role
from deskflow.db.passwords import hash_password, verify_password


def test_password_round_trip() -> None:
    stored = hash_password("sample")
    assert stored.startswith("pbkdf2_sha256$")
    assert verify_password("sample", stored)
    assert not verify_password("other", stored)


def test_primary_role_prefers_exec() -> None:
    assert primary_role(["candidate", "exec", "recruiter"]) == "exec"
    assert primary_role(["candidate", "recruiter"]) == "recruiter"
    assert primary_role([]) == "visitor"
