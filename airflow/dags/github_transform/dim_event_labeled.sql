---
operator: operators.SqlToWarehouseOperator
dst_table_name: dim_event_labeled
---

SELECT
    json ->> 'type' AS type,
    json ->> 'id' AS id,
    json ->> '$.actor.id' AS actor_id,
    json ->> '$.label.id' AS label_id,
    json ->> '$.labelable.id' AS labelable_id,
    json ->> 'createdAt' AS created_at,
FROM {{ ref("stg_issue_events") }}
WHERE type = 'LabeledEvent'

