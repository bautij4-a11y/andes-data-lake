# Andes Data Lake

A miniature, open-source corporate data platform built to practice end-to-end data engineering.

It simulates an industrial company with two typical data sources:

- **SAP-like transactional data**: materials, purchase orders, sales and maintenance.
- **SCADA-like sensor data**: near real-time readings such as temperature, pressure and flow.

The platform ingests, processes, validates, catalogs and serves this data for analytics and AI.

## Goals

- Build a complete data pipeline using only open-source technologies.
- Cover ingestion, data lake layers (bronze/silver/gold), distributed processing, orchestration, data quality and governance.
- Produce reproducible, documented work: one command should bring the environment up.

## Planned stack

Kafka, NiFi, MinIO, Spark, Hive, Trino, Airflow, Great Expectations, OpenMetadata, Superset, Docker.

## Status

Phase 0: environment setup (WSL2, Docker, Git, repository structure).

## Repository layout

| Folder | Purpose |
|---|---|
| `docs/` | Architecture and technical decisions |
| `infra/` | Docker Compose files and service configuration |
| `sources/` | Simulated data generators (SAP and SCADA) |
| `ingestion/` | Kafka and NiFi flows |
| `processing/` | Spark jobs |
| `orchestration/` | Airflow DAGs |
| `quality/` | Data quality checks |
| `governance/` | Catalog and lineage |
| `analytics/` | Datasets and dashboards for BI and AI |
| `tests/` | Automated tests |
