import os
import re

from airflow.models import BaseOperator, Variable

from operators.sql_to_warehouse_operator import render_template, _ref
from functools import partial


# TODO: copied from sql_to_warehouse
def detect_dependencies(sql):
    return re.findall(r'''ref\(\s*"(.*?)"\s*\)''', sql)


# for duckdb, this will just query parquet back to parquet
class SqlQueryOperator(BaseOperator):

    def __init__(
        self,
        sql: str,
        schema: "str | None" = None,
        fields=None,
        **kwargs
    ):
        self.sql = sql
        self.schema = schema

        if fields is not None:
            raise NotImplementedError()

        super().__init__(**kwargs)

        self.dependencies = detect_dependencies(self.sql)

    def execute(self, context):
        from sqlalchemy import create_engine

        this = f"{self.schema}.{self.task_id}"

        xcom_vals = context["ti"].xcom_pull(task_ids = self.dependencies)
        table_deps = dict(zip(self.dependencies, xcom_vals))
        sql = render_template(
            self.sql,
            ref = partial(_ref, mappings=table_deps),
            this = this,
            ds = context["ds"]
        )

        engine = create_engine(Variable.get("PIPELINE_WAREHOUSE_URI"))
        engine.execute(sql)

        return this

        
