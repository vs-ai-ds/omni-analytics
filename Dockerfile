# Dockerfile
# Purpose: Build the Python app image used by compose ("app" service).
# Notes:
# - Installs minimal system packages for psycopg/lxml/etc.
# - Installs Python dependencies from requirements.txt
# - Copies your source code into /app

FROM python:3.11-slim

# --- System deps for psycopg, lxml, tzdata, etc. ---
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential libpq-dev gcc     libxml2-dev libxslt1-dev     ca-certificates curl tzdata     && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependency list first (for better layer caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Default command: a safe no-op (we'll run ad-hoc via compose exec)
CMD ["python", "-m", "src.jobs.manage", "healthcheck"]
