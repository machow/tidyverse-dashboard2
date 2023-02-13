---
operator: operators.SqlToWarehouseOperator
dst_table_name: dim_event_comment_deleted
---

SELECT
    json ->> 'type' AS type,
    json ->> 'id' AS id,
    json ->> '$.actor.id' AS actor_id,
    json ->> 'createdAt' AS created_at,
    json ->> 'databaseId' AS database_id,
    json ->> '$.deletedCommentAuthor.id' AS author_id,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'CommentDeletedEvent'
