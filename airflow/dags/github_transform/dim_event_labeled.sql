---
operator: operators.SqlToWarehouseOperator
schema: github_extract
---

SELECT
    issue_id,
    type,
    JSON_EXTRACT(data, '$.id') AS id,
    JSON_EXTRACT(data, '$.actor.id') AS actor_id,
    JSON_EXTRACT(data, '$.label.id') AS label_id,
    JSON_EXTRACT(data, '$.labelable.id') AS labelable_id,
    JSON_EXTRACT(data, '$.createdAt') AS created_at,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'LabeledEvent'

