# ---
# python_callable: main
# provide_context: true
# op_kwargs:
#   schema: github_extract
# python_callable_partials:
#   stg_commits:
#     file_name: commits.parquet
#   stg_issue_comments:
#     file_name: issue_comments.parquet
#   stg_issue_labels:
#     file_name: issue_labels.parquet
#   stg_issues:
#     file_name: issues.parquet
#   stg_issues_pr:
#     file_name: issues_pr.parquet
#   stg_labels:
#     file_name: labels.parquet
#   stg_pull_requests:
#     file_name: pull_requests.parquet
#   stg_repository:
#     file_name: repository.parquet
#   stg_stargazers:
#     file_name: stargazers.parquet
# ---


def main(file_name, schema, ds, **kwargs):
    import pendulum

    from dbpal.utils import file_to_warehouse
    from utils import previous_date

    table_name = "stg_" + file_name.rsplit(".")[0]
    full_name = f"{schema}.{table_name}"
    res_table = file_to_warehouse(f"github_extract/dt={ds}/*/{file_name}", full_name)

    print("Resulting table:", full_name)

    return full_name

