import os
import airflow

from gusty import create_dag
from pathlib import Path

#####################
## DAG Directories ##
#####################

# point to your dags directory
dag_parent_dir = Path(__file__).parent

# assumes any subdirectories in the dags directory are Gusty DAGs (with METADATA.yml)
# (excludes subdirectories like __pycache__)
# copied from: https://github.com/cal-itp/data-infra/blob/main/airflow/dags/dags.py
dag_directories = []
for child in dag_parent_dir.iterdir():
    if child.is_dir() and not str(child).endswith("__"):
        dag_directories.append(str(child))


####################
## DAG Generation ##
####################

# TODO: move out of this file
def _ref(name):
    import os
    from dbpal.config import get_sql_engine

    warehouse_path = os.environ["PIPELINE_WAREHOUSE_URI"]
    engine = get_sql_engine()

    if engine.name == "duckdb":
        return f"""read_parquet("{warehouse_path}/{name}.parquet")"""

    else:
        return name


def get_var(name):
    from airflow.models import Variable

    try:
        return Variable.get(name)
    except KeyError:
        print(f"WARNING: no variable named {name} found")


for dag_directory in dag_directories:
    dag_id = os.path.basename(dag_directory)
    globals()[dag_id] = create_dag(
        dag_directory,
        tags = ['default', 'tags'],
        task_group_defaults={"tooltip": "this is a default tooltip"},
        wait_for_defaults={
            "retries": 10,
            "check_existence": True
        },
        latest_only=False,
        user_defined_macros={
            "ref": _ref,
        },
        dag_constructors={
            "get_var": get_var
        },
    )
