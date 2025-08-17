-- Purpose: Initialize database schemas and a tiny meta table.
-- This script runs automatically when the postgres container starts
-- for the first time (mounted into /docker-entrypoint-initdb.d).

CREATE SCHEMA IF NOT EXISTS src;
CREATE SCHEMA IF NOT EXISTS dw;
CREATE SCHEMA IF NOT EXISTS stg;
CREATE SCHEMA IF NOT EXISTS meta;

-- UUIDs and crypto helpers (available in official Postgres images)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Simple run-tracking table for pipelines
CREATE TABLE IF NOT EXISTS meta.etl_runs (
  run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_name TEXT NOT NULL,
  started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  finished_at TIMESTAMPTZ,
  status TEXT CHECK (status IN ('started','success','failed')) NOT NULL DEFAULT 'started',
  rows_in BIGINT,
  rows_out BIGINT,
  checksum TEXT
);
