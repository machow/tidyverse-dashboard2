---
operator: operators.SqlToWarehouseOperator
dst_table_name: dim_event_closed
---

SELECT
    json ->> 'type' AS type,
    json ->> 'id' AS id,
    json ->> '$.actor.id' AS actor_id,
    json ->> 'created_at' AS created_at,
    json ->> '$.closable.closed' AS is_closed,
    json ->> '$.closable.closedAt' AS closed_at,
    json ->> '$.closable.id' AS issue_id,
    json ->> '$.closer.id' AS closer_id,
    json ->> '$.closer.type' AS closer_type,
    json ->> 'stateReason' AS state_reason,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'ClosedEvent'
