---
operator: operators.SqlToWarehouseOperator
dst_table_name: dim_event_assigned
---

SELECT
    json ->> 'type' AS type,
    json ->> 'id' AS id,
    json -> '$.assignable.id' AS assignable_id,
    json -> '$.assignee.id' AS assignee_id,
    json -> 'created_at' AS created_at,
    json -> '$.user.id' AS user_id
FROM {{ ref("stg_issue_events") }}
WHERE type = 'AssignedEvent'
