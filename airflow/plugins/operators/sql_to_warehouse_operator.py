import os
import re

from airflow.models import BaseOperator, Variable
from functools import partial
from pathlib import Path


def detect_dependencies(sql):
    return re.findall(r'''ref\(\s*"(.*?)"\s*\)''', sql)


def render_template(template, **user_defined_macros):
    from jinja2 import Environment

    env = Environment()
    #env.filters = {**env.filters, **filters}

    template = env.from_string(template)

    return template.render({**user_defined_macros})


def _ref(name, mappings):
    return mappings.get(name)


# for duckdb, this will just query parquet back to parquet
class SqlToWarehouseOperator(BaseOperator):
    #template_fields = ("sql",)

    def __init__(
        self,
        task_id: str,
        sql: str,
        schema: str,
        dst_table_name: "str | None" = None,
        fields=None,
        **kwargs
    ):
        self.sql = sql
        self.schema = schema
        self.dst_table_name = dst_table_name

        if fields is not None:
            raise NotImplementedError()

        super().__init__(task_id = task_id, **kwargs)

        self.dependencies = detect_dependencies(self.sql)

    def execute(self, context):
        from sqlalchemy import create_engine
        from dbpal.utils import copy_to_warehouse

        table_name = self.dst_table_name if self.dst_table_name else self.task_id
        full_name = f"{self.schema}.{table_name}"

        xcom_vals = context["ti"].xcom_pull(task_ids = self.dependencies)
        table_deps = dict(zip(self.dependencies, xcom_vals))

        sql = render_template(self.sql, ref = partial(_ref, mappings=table_deps))

        engine = create_engine(Variable.get("PIPELINE_WAREHOUSE_URI"))
        result_table_name = copy_to_warehouse(sql, full_name, engine)

        print("Resulting table name:", result_table_name)
        return result_table_name
