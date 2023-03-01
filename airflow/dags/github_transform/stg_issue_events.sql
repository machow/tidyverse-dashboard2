---
operator: operators.SqlQueryOperator
schema: github_extract
---

LOAD DATA OVERWRITE {{ this }} (
    issue_id STRING,
    type STRING,
    data JSON
)
FROM FILES (
  format = 'JSON',
  uris = ['gs://tidyverse-pipeline/github_extract/dt={{ds}}/*/issue_events.ndjson']
)
