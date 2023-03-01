---
operator: operators.SqlToWarehouseOperator
schema: github_extract
---

SELECT *, FALSE AS is_pull_request FROM {{ ref("stg_issues") }}
UNION ALL
SELECT *, TRUE AS is_pull_request FROM {{ ref("stg_issues_pr") }}

