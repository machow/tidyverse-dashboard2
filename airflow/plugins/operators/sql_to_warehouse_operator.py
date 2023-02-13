import os
import re

from airflow.models import BaseOperator
from pathlib import Path


def detect_dependencies(sql):
    return re.findall(r'''ref\(\s*"(.*?)"\s*\)''', sql)


# for duckdb, this will just query parquet back to parquet
class SqlToWarehouseOperator(BaseOperator):
    template_fields = ("sql",)

    def __init__(
        self,
        sql,
        dst_table_name,
        fields=None,
        **kwargs
    ):
        self.sql = sql
        self.dst_table_name = dst_table_name

        if fields is not None:
            raise NotImplementedError()

        super().__init__(**kwargs)

        self.dependencies = detect_dependencies(self.sql)

    def execute(self, context):
        from tidypal.utils import copy_to_warehouse
        copy_to_warehouse(self.sql, self.dst_table_name)
