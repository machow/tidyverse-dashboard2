---
operator: operators.SqlToWarehouseOperator
schema: github_extract
---

SELECT
    issue_id
    type,
    STRING(JSON_EXTRACT(data, '$.id')) AS id,
    STRING(JSON_EXTRACT(data, '$.actor.id')) AS actor_id,
    PARSE_DATETIME('%FT%TZ', JSON_EXTRACT_SCALAR(data, '$.createdAt')) AS created_at,
    INT64(JSON_EXTRACT(data, '$.databaseId')) AS database_id,
    STRING(JSON_EXTRACT(data, '$.deletedCommentAuthor.id')) AS author_id,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'CommentDeletedEvent'
