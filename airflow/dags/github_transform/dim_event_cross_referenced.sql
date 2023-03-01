---
operator: operators.SqlToWarehouseOperator
schema: github_extract
---

SELECT
    issue_id,
    type,
    JSON_EXTRACT(data, '$.id') AS id,
    JSON_EXTRACT(data, '$.actor.id') AS actor_id,
    JSON_EXTRACT(data, '$.createdAt') AS created_at,
    JSON_EXTRACT(data, '$.isCrossRepository') AS is_cross_repository,
    JSON_EXTRACT(data, '$.referencedAt') AS referenced_at,
    JSON_EXTRACT(data, '$.source.id') AS source_id,
    JSON_EXTRACT(data, '$.target.id') AS target_id,
    JSON_EXTRACT(data, '$.willCloseTarget') AS will_close_target,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'CrossReferencedEvent'
