"""
Purpose: Create a single SQLAlchemy engine for DB access.
All DB-using modules should import get_engine() so we keep connection logic DRY.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from .config import Settings, load_yaml, build_db_url

def get_engine() -> Engine:
    """
    Build and return a SQLAlchemy Engine using project configuration.
    - Reads .env for secrets (host/user/pass)
    - Reads settings.yaml for template URL
    - Respects the 'echo_sql' flag to log SQL for debugging
    """
    env = Settings()
    cfg = load_yaml("config/settings.yaml")
    url = build_db_url(cfg, env)
    echo = bool(cfg["database"].get("echo_sql", False))
    engine = create_engine(url, echo=echo, future=True)
    return engine

def ping() -> bool:
    """
    Lightweight health check against the DB.
    Returns True on success, raises on failure.
    """
    eng = get_engine()
    with eng.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True
