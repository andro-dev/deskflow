from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from deskflow.config import get_settings
from deskflow.db.models import Base

_engine: Engine | None = None
SessionLocal: sessionmaker[Session] | None = None

REPO_ROOT = Path(__file__).resolve().parents[3]


def _sqlite_url(url: str) -> str:
    if url.startswith("sqlite:///") and not url.startswith("sqlite:////"):
        path = url.removeprefix("sqlite:///")
        if path in {":memory:", ""}:
            return url
        db_path = Path(path)
        if not db_path.is_absolute():
            db_path = REPO_ROOT / db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_path}"
    return url


@event.listens_for(Engine, "connect")
def _sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:  # type: ignore[no-untyped-def]
    module = getattr(dbapi_connection, "__class__", type("x", (), {})).__module__
    if "sqlite" in module:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def reset_engine() -> None:
    global _engine, SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    SessionLocal = None


def get_engine() -> Engine:
    global _engine, SessionLocal
    if _engine is None:
        url = _sqlite_url(get_settings().database_url)
        kwargs: dict = {}
        if url.startswith("sqlite"):
            kwargs["connect_args"] = {"check_same_thread": False}
        _engine = create_engine(url, **kwargs)
        SessionLocal = sessionmaker(bind=_engine, expire_on_commit=False)
    assert SessionLocal is not None
    return _engine


def session_factory() -> sessionmaker[Session]:
    get_engine()
    assert SessionLocal is not None
    return SessionLocal


def get_session() -> Generator[Session, None, None]:
    db = session_factory()()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db(*, drop: bool = False) -> None:
    from deskflow.db.seed import seed_if_empty

    engine = get_engine()
    if drop:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    seed_if_empty()
