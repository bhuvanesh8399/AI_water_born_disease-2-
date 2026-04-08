# Data Layout

`backend/data/core`

- Canonical CSVs used by the active backend ingestion and pipeline flows.
- Expected files:
  - `district_master.csv`
  - `district_profile.csv`
  - `observations_base.csv`
  - `historical_alerts.csv`

`backend/data/enrichment`

- Reference and enrichment datasets used to build district enrichment tables.
- Includes Tamil Nadu and India-wide demographic, sanitation, water, health, and vulnerability sources.

`backend/data/archive`

- Duplicate files, alternate schemas, or older extracts kept for reference only.
- These should not be treated as canonical ingestion inputs.
