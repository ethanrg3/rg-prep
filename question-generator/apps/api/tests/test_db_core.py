from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import core as db_core


def test_get_db_engine_returns_engine() -> None:
    engine = db_core.get_db_engine()
    assert isinstance(engine, Engine)


def test_get_db_session_can_execute_and_close() -> None:
    sess = db_core.get_db_session()
    assert isinstance(sess, Session)
    result = sess.execute("SELECT 1").scalar()
    assert int(result) == 1
    sess.close()


def test_get_db_generator_yields_session_and_closes() -> None:
    gen = db_core.get_db()
    db = next(gen)
    assert isinstance(db, Session)
    # simple query to ensure session works
    db.execute("SELECT 1")
    # close generator to run the finally block which closes the session
    gen.close()


def test_init_db_creates_tables(tmp_path) -> None:
    # Keep originals so we can restore after the test
    orig_engine = db_core._engine
    orig_session_local = db_core._SessionLocal

    try:
        db_file = tmp_path / "test.db"
        url = f"sqlite:///{db_file}"
        engine = create_engine(url, connect_args={"check_same_thread": False})

        # Patch module-level engine and sessionmaker
        db_core._engine = engine
        db_core._SessionLocal = sessionmaker(bind=engine)

        # Define a test model that will register itself with Base.metadata
        from sqlalchemy import Column, Integer

        class TestModel(db_core.Base):
            __tablename__ = "test_model"
            id = Column(Integer, primary_key=True)

        # ensure the table doesn't exist yet
        inspector = inspect(engine)
        assert "test_model" not in inspector.get_table_names()

        # create tables
        db_core.init_db()

        inspector = inspect(engine)
        assert "test_model" in inspector.get_table_names()

    finally:
        # Restore original engine/session to avoid side effects
        db_core._engine = orig_engine
        db_core._SessionLocal = orig_session_local
