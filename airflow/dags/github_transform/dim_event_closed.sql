---
operator: operators.SqlToWarehouseOperator
schema: github_extract
---

SELECT
    issue_id,
    type,
    STRING(JSON_EXTRACT(data, '$.id')) AS id,
    STRING(JSON_EXTRACT(data, '$.actor.id')) AS actor_id,
    PARSE_DATETIME('%FT%TZ', JSON_EXTRACT_SCALAR(data, '$.created_at')) AS created_at,
    BOOL(JSON_EXTRACT(data, '$.closable.closed')) AS is_closed,
    PARSE_DATETIME('%FT%TZ', JSON_EXTRACT_SCALAR(data, '$.closable.closedAt')) AS closed_at,
    STRING(JSON_EXTRACT(data, '$.closable.id')) AS closable_id,
    STRING(JSON_EXTRACT(data, '$.closer.id')) AS closer_id,
    STRING(JSON_EXTRACT(data, '$.closer.type')) AS closer_type,
    STRING(JSON_EXTRACT(data, '$.stateReason')) AS state_reason,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'ClosedEvent'
