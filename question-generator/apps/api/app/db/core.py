"""
Database core configuration and session management.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.settings import settings

DATABASE_URL = settings.database_url

# For SQLite we need to disable the same-thread check when using the DB
# from multiple threads (e.g. in tests or with a web worker).
CONNECT_ARGS = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite:") else {}

# Module-level engine and session factory to avoid recreating them on every call
_engine: Engine = create_engine(DATABASE_URL, future=True, connect_args=CONNECT_ARGS)
_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine, future=True)


class Base(DeclarativeBase):
    """All ORM models will inherit from this class."""


def get_db_engine() -> Engine:
    """Return the module-level SQLAlchemy engine."""
    return _engine


def get_db_session() -> Session:
    """Return a new Session instance (not a dependency). Caller must close it."""
    return _SessionLocal()


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after use.

    Intended for use as a FastAPI dependency::

        async def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db: Session = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create database tables for all declarative models.

    Useful for tests or a simple local setup that uses SQLite.
    """
    Base.metadata.create_all(bind=_engine)
