"""
Purpose: Centralized configuration utilities.
- Reads environment variables from .env (via pydantic-settings)
- Reads structured config from YAML (settings.yaml)
- Builds a SQLAlchemy Postgres URL for the app to use.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import yaml

class Settings(BaseSettings):
    """
    Loads env vars from .env. We keep secrets (DB password) out of source code.
    Any variable in .env that matches these names will be available here.
    """
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: str = "dev"
    TZ: str = "UTC"
    PG_HOST: str = Field(default="postgres")
    PG_PORT: int = Field(default=5432)
    PG_DB: str = Field(default="omni_dw")
    PG_USER: str = Field(default="omni_user")
    PG_PASSWORD: str = Field(default="omni_pass")

def load_yaml(path: str) -> dict:
    """
    Read a YAML file and return a Python dict.
    Used for non-secret, human-readable settings (paths, feature flags).
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_db_url(cfg: dict, env: Settings) -> str:
    """
    Compose the SQLAlchemy Postgres URL using values from settings.yaml + .env.
    Example output: postgresql+psycopg://user:pass@host:5432/dbname
    """
    url_tpl = cfg["database"]["url"]
    return url_tpl.format(
        user=env.PG_USER,
        password=env.PG_PASSWORD,
        host=env.PG_HOST,
        port=env.PG_PORT,
        db=env.PG_DB,
    )
