from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.core.settigs import settings


def get_db_engine() -> Engine:
    db_url = settings.database_url
    return create_engine(db_url)
