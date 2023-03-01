---
operator: operators.SqlToWarehouseOperator
schema: github_extract
---

SELECT
    issue_id,
    type,
    JSON_EXTRACT(data, '$.id') AS id,
    JSON_EXTRACT(data, '$.assignable.id') AS assignable_id,
    JSON_EXTRACT(data, '$.assignee.id') AS assignee_id,
    JSON_EXTRACT(data, '$.created_at') AS created_at,
    JSON_EXTRACT(data, '$.user.id') AS user_id
FROM {{ ref("stg_issue_events") }}
WHERE type = 'AssignedEvent'
