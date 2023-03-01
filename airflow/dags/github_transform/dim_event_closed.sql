---
operator: operators.SqlToWarehouseOperator
schema: github_extract
---

SELECT
    issue_id,
    type,
    JSON_EXTRACT(data, '$.id') AS id,
    JSON_EXTRACT(data, '$.actor.id') AS actor_id,
    JSON_EXTRACT(data, '$.created_at') AS created_at,
    JSON_EXTRACT(data, '$.closable.closed') AS is_closed,
    JSON_EXTRACT(data, '$.closable.closedAt') AS closed_at,
    JSON_EXTRACT(data, '$.closable.id') AS closable_id,
    JSON_EXTRACT(data, '$.closer.id') AS closer_id,
    JSON_EXTRACT(data, '$.closer.type') AS closer_type,
    JSON_EXTRACT(data, '$.stateReason') AS state_reason,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'ClosedEvent'
