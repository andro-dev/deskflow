from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from deskflow.app import app
from deskflow.db.engine import init_db, reset_engine
from deskflow.proto import store

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def isolated_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.setenv("DESKFLOW_DATABASE_URL", f"sqlite:///{tmp_path / 'deskflow.sqlite'}")
    monkeypatch.setenv("DESKFLOW_ENV", "test")
    reset_engine()
    init_db()
    yield
    reset_engine()


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def strong_payload() -> dict:
    return json.loads((ROOT / "samples" / "strong_fit_sdet.json").read_text())


@pytest.fixture
def weak_payload() -> dict:
    return json.loads((ROOT / "samples" / "weak_fit_manual_qa.json").read_text())
