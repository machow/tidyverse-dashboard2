---
operator: operators.SqlToWarehouseOperator
schema: github_extract
---

SELECT
    issue_id
    type,
    JSON_EXTRACT(data, '$.id') AS id,
    JSON_EXTRACT(data, '$.actor.id') AS actor_id,
    JSON_EXTRACT(data, '$.createdAt') AS created_at,
    JSON_EXTRACT(data, '$.databaseId') AS database_id,
    JSON_EXTRACT(data, '$.deletedCommentAuthor.id') AS author_id,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'CommentDeletedEvent'
