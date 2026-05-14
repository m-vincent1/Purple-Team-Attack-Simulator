import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.main import app, _seed_scenarios, _seed_rules


@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    _seed_scenarios(session)
    _seed_rules(session)
    yield session
    session.close()


@pytest.fixture(scope="function")
def client(tmp_path):
    # Use a real temp SQLite file so lifespan can init and seed it normally
    db_file = tmp_path / "test_purple_team.db"
    db_url = f"sqlite:///{db_file}"

    import app.core.database as db_module
    import app.core.config as config_module

    original_url = config_module.settings.DATABASE_URL
    original_engine = db_module.engine
    original_session = db_module.SessionLocal

    # Build new engine/session pointing to temp file
    test_engine = create_engine(db_url, connect_args={"check_same_thread": False})
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    # Patch at module level so lifespan picks up the new engine
    db_module.engine = test_engine
    db_module.SessionLocal = TestSession

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Create tables manually before lifespan (lifespan will also try, idempotent)
    Base.metadata.create_all(bind=test_engine)

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    db_module.engine = original_engine
    db_module.SessionLocal = original_session
