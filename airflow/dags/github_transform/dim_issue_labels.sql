---
operator: operators.SqlToWarehouseOperator
schema: github_extract
---

SELECT
    labels.id,
    labels.color,
    labels.description,
    labels.is_default,
    labels.name,
    labels.url,
    labels.repository_id,
    issue_labels.issue_id,
    issue_labels.label_id,
FROM {{ ref("stg_issue_labels") }} issue_labels
LEFT JOIN {{ ref("stg_labels") }} labels
    ON issue_labels.label_id = labels.id
