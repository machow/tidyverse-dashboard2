---
operator: operators.SqlQueryOperator
schema: pypi_extract
multi_task_spec:
  siuba: {}
#  shiny: {}
#  vetiver: {}
#  htmltools: {}
#  guildai: {}
#  plotnine: {}
#  dash: {}

---

EXPORT DATA OPTIONS (
  uri = 'gs://tidyverse-pipeline/pypi-extract/project={{task_id}}/dt={{ds}}/*',
  format = 'PARQUET',
  overwrite=true
)

SELECT *
FROM `bigquery-public-data.pypi.file_downloads`
WHERE 
    file.project = {{ task_id }}
    AND CAST(timestamp AS DATE) = {{ ds }}
GROUP BY 1, 2, 3
