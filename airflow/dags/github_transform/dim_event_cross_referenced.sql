---
operator: operators.SqlToWarehouseOperator
dst_table_name: dim_event_cross_referenced
---

SELECT
    json ->> 'type' AS type,
    json ->> 'id' AS id,
    json ->> '$.actor.id' AS actor_id,
    json ->> 'createdAt' AS created_at,
    json ->> 'isCrossRepository' AS is_cross_repository,
    json ->> 'referencedAt' AS referenced_at,
    json ->> '$.source.id' AS source_id,
    json ->> '$.target.id' AS target_id,
    json ->> 'willCloseTarget' AS will_close_target,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'CrossReferencedEvent'
