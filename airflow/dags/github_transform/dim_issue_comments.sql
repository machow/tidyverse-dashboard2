---
operator: operators.SqlToWarehouseOperator
schema: github_extract
---

SELECT
    issue_id,
    type,
    JSON_EXTRACT(data, '$.id') AS id,
    JSON_EXTRACT(data, '$.author.user_id') AS user_id,
    JSON_EXTRACT(data, '$.body') AS body,
    JSON_EXTRACT(data, '$.created_at') AS created_at,
    JSON_EXTRACT(data, '$.updated_at') AS updated_at,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'IssueComment'
