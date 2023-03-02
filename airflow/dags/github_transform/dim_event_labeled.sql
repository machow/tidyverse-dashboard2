---
operator: operators.SqlToWarehouseOperator
schema: github_extract
---

SELECT
    issue_id,
    type,
    STRING(JSON_EXTRACT(data, '$.id')) AS id,
    STRING(JSON_EXTRACT(data, '$.actor.id')) AS actor_id,
    STRING(JSON_EXTRACT(data, '$.label.id')) AS label_id,
    STRING(JSON_EXTRACT(data, '$.labelable.id')) AS labelable_id,
    PARSE_DATETIME('%FT%TZ', JSON_EXTRACT_SCALAR(data, '$.createdAt')) AS created_at,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'LabeledEvent'

