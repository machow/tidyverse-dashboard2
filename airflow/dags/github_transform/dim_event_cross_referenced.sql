---
operator: operators.SqlToWarehouseOperator
schema: github_extract
---

SELECT
    issue_id,
    type,
    STRING(JSON_EXTRACT(data, '$.id')) AS id,
    STRING(JSON_EXTRACT(data, '$.actor.id')) AS actor_id,
    PARSE_DATETIME('%FT%TZ', JSON_EXTRACT_SCALAR(data, '$.createdAt')) AS created_at,
    BOOL(JSON_EXTRACT(data, '$.isCrossRepository')) AS is_cross_repository,
    PARSE_DATETIME('%FT%TZ', JSON_EXTRACT_SCALAR(data, '$.referencedAt')) AS referenced_at,
    STRING(JSON_EXTRACT(data, '$.source.id')) AS source_id,
    STRING(JSON_EXTRACT(data, '$.target.id')) AS target_id,
    BOOL(JSON_EXTRACT(data, '$.willCloseTarget')) AS will_close_target,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'CrossReferencedEvent'
