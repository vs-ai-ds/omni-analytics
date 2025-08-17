# Project Skeleton + Environment Setup

This repository uses Docker to run Postgres, pgAdmin, an SFTP server, and the Python app
in isolated containers. Follow the Windows quick start below.

## Prerequisites
- Docker Desktop for Windows (enable **WSL 2 based engine**)
- Git
- Internet access (to pull images from Docker Hub)

> Note: Docker is a system prerequisite — it’s **not** listed in `requirements.txt`.

## Windows Quick Start

1) Prepare Windows for Docker/WSL 2 (PowerShell **as Administrator**):

   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   wsl --set-default-version 2
   ```
   Reboot if asked. Install/launch Docker Desktop (should show Running).

2) 
   ```bash
   Copy `.env.example` → `.env`
   ```

3) Start the stack:
   ```bash
   docker compose build app
   docker compose up -d
   ```
   Expected: SUCCESS: Stack is up and DB connection OK.

4) Smoke test DB connectivity from inside the app container:
   ```bash
   docker compose exec app python -m src.jobs.manage healthcheck
   ```
   Expected: `DB connection OK`. Check logs at `logs/app.log`.


## Services
- **postgres**: Postgres 15 (exposed on `localhost:5432` for Power BI).
- **pgadmin**: DB admin UI at `localhost:5050`.
- **sftp**: SFTP server at `localhost:2222` (uploads land in `data/landing/ftp`).
- **app**: Python 3.11 container with all dependencies. Code is mounted live into it.

## Common Commands
   ```bash
      docker compose ps                 REM show containers
      docker compose logs -f            REM tail logs
      docker compose down               REM stop containers
      docker compose down -v            REM stop + delete DB volume (full reset)
   ```
## How to run future jobs (examples used in later steps)
   ```bash
      docker compose exec app python -m src.jobs.manage seed-oltp --months 24
      docker compose exec app python -m src.jobs.manage ingest --source amazon --date 2025-08-17
      docker compose exec app python -m src.jobs.manage load-dw --since 2024-01-01
   ```

## File/Folder Summary
- **.env.example** — Template for secrets/connection strings. Copy to `.env`.
- **Dockerfile** — Builds the Python app image (reproducible runtime).
- **docker-compose.yml** — Orchestrates Postgres/pgAdmin/SFTP/App.
- **config/** — Central settings (YAML) and logging config.
- **sql/bootstrap/00_init.sql** — Creates base schemas and meta tables at DB start.
- **src/common/** — Shared code for configuration and DB connections.
- **src/jobs/manage.py** — CLI entry to run tasks like `healthcheck`.
- **data/** — Landing (raw), staging (Parquet), etc. for pipeline files.
- **pbi/** — Place the PBIX here later.
