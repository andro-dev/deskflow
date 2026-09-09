from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from deskflow.app import app

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def strong_payload() -> dict:
    return json.loads((ROOT / "samples" / "strong_fit_sdet.json").read_text())


@pytest.fixture
def weak_payload() -> dict:
    return json.loads((ROOT / "samples" / "weak_fit_manual_qa.json").read_text())
