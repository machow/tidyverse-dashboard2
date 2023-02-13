---
operator: operators.SqlToWarehouseOperator
dst_table_name: dim_issues
---

SELECT *, FALSE AS is_pull_request FROM {{ ref("stg_issues") }}
UNION ALL
SELECT *, TRUE AS is_pull_request FROM {{ ref("stg_issues_pr") }}

