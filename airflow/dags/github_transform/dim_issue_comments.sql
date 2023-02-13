---
operator: operators.SqlToWarehouseOperator
dst_table_name: dim_issue_comments
---

SELECT
    json ->> 'type' AS type,
    json ->> 'id' AS id,
    json -> '$.issue.id' AS issue_id,
    json -> '$.author.user_id' AS user_id,
    json -> '$.body' AS body,
    json -> 'created_at' AS created_at,
    json -> 'updated_at' AS updated_at,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'IssueComment'
