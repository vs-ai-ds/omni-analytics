"""
Purpose: Small CLI to run project jobs (healthcheck, seeders, ingestors).
Add new subcommands here (e.g., seed-oltp, ingest-files, load-dw).
"""

import argparse
from loguru import logger
from sqlalchemy import text
from src.common.db import get_engine

def cmd_healthcheck():
    """
    Verifies we can connect to Postgres and execute a trivial query.
    Helpful as a first 'smoke test' after bringing up Docker or local DB.
    """
    eng = get_engine()
    with eng.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info("DB connection OK")

def main():
    """
    CLI entry point.
    Usage:
      docker compose exec app python -m src.jobs.manage healthcheck
    """
    parser = argparse.ArgumentParser(prog="omni-cli")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Register subcommands
    sub.add_parser("healthcheck")

    args = parser.parse_args()

    if args.cmd == "healthcheck":
        cmd_healthcheck()

if __name__ == "__main__":
    main()
