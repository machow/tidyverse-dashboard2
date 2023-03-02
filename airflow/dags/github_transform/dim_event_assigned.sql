---
operator: operators.SqlToWarehouseOperator
schema: github_extract
---

SELECT
    issue_id,
    type,
    STRING(JSON_EXTRACT(data, '$.id')) AS id,
    STRING(JSON_EXTRACT(data, '$.assignable.id')) AS assignable_id,
    STRING(JSON_EXTRACT(data, '$.assignee.id')) AS assignee_id,
    PARSE_DATETIME('%F', JSON_EXTRACT_SCALAR(data, '$.created_at')) AS created_at,
    STRING(JSON_EXTRACT(data, '$.user.id')) AS user_id
FROM {{ ref("stg_issue_events") }}
WHERE type = 'AssignedEvent'
