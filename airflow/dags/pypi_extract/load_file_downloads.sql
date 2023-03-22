---
operator: operators.SqlQueryOperator
schema: pypi_extract
dependencies:
  - latest_only
---

CREATE OR REPLACE EXTERNAL TABLE `{{schema}}`.`file_downloads`
WITH PARTITION COLUMNS (
  project_name STRING,
  dt DATE
)
OPTIONS (
  uris = ['gs://tidyverse-pipeline/pypi-extract/*'],
  format = "PARQUET",
  hive_partition_uri_prefix = 'gs://tidyverse-pipeline/pypi-extract',
  require_hive_partition_filter = false
)
  
