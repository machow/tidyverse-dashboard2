---
operator: operators.SqlQueryOperator
schema: pypi_extract
location: US
multi_task_spec:
  siuba: {}
  streamlit: {}
  pins: {}
  shiny: {}
  vetiver: {}
  htmltools: {}
  guildai: {}
  plotnine: {}
  dash: {}
  quartodoc: {}
  bentoml: {}

---

EXPORT DATA OPTIONS (
  uri = 'gs://tidyverse-pipeline/pypi-extract/project_name={{task_id}}/dt={{ds}}/*.parquet',
  format = 'PARQUET',
  overwrite=true
) AS

SELECT *
FROM `bigquery-public-data.pypi.file_downloads`
WHERE 
    file.project = '{{ task_id }}'
    AND CAST(timestamp AS DATE) = '{{ ds }}'
