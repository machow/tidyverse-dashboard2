import os
import logging
import siuba as sb
import pandas as pd

from dataclasses import dataclass
from functools import singledispatch, lru_cache
from pathlib import Path
from siuba.sql import LazyTbl
from sqlalchemy import create_engine

from tidypal import get_sql_engine, get_bucket

SQL_DUCKDB_TEMPLATE = """
COPY (

{sql}

)
TO '{name}.parquet' (FORMAT 'parquet')
"""

SQL_TEMPLATE = """CREATE OR REPLACE TABLE "{name}" AS {tbl}"""


def compile_sql(tbl: LazyTbl):
    sel = tbl.last_select
    compiled = sel.compile(
        dialect = tbl.source.dialect,
        compile_kwargs = {"literal_binds": True}
    )

    return str(compiled)


@lru_cache(maxsize=None)
def get_sql_engine():
    uri = os.environ["PIPELINE_WAREHOUSE_URI"]

    ENGINE_URI = f"duckdb:///:memory:"
    return create_engine(ENGINE_URI)


# copy_to_warehouse ===========================================================

@singledispatch
def copy_to_warehouse(tbl, name: str):
    raise TypeError(f"Cannot copy data of type `{type(tbl)}` to warehouse")


@copy_to_warehouse.register
def _ctw(tbl: LazyTbl, name):
    compiled = compile_sql(data)

    create_stmt = f"""CREATE OR REPLACE TABLE "{name}" AS {compiled}"""

    engine = get_sql_engine()
    engine.execute(create_stmt)
    

@copy_to_warehouse.register
def _ctw(tbl: pd.DataFrame, name):
    engine = get_sql_engine()

    sql_tbl = engine.connect().connection.c.from_df(tbl)

    # note that duckdbs create method can't replace :/
    engine.execute(f"""DROP TABLE IF EXISTS "{name}" """)
    sql_tbl.create(name)
    

@copy_to_warehouse.register
def _ctw(tbl: str, name: str):
    engine = get_sql_engine()

    # TODO: use something like dbcooper-py generic dispatch use name for dispatch
    if engine.dialect.name == "duckdb":
        # just create parquet files on disk
        warehouse_path = os.environ["PIPELINE_WAREHOUSE_URI"]

        Path(warehouse_path).mkdir(exist_ok=True)

        final_name = warehouse_path + "/" + name
        create_stmt = SQL_DUCKDB_TEMPLATE.format(sql=tbl, name = final_name)

    else:
        create_stmt = SQL_TEMPLATE.format(sql=tbl, name=name)

    print("doing stuff")
    logging.info(create_stmt)

    engine.execute(create_stmt)


# File to warehouse ===========================================================

# data classes ----

class File:
    _registry = {}
    suffix = None

    def __init__(self, name: str):
        self.name = name

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)

        if cls.suffix in cls._registry:
            raise KeyError("Suffix {cls.suffix} already in registry")

        cls._registry[cls.suffix] = cls

    @classmethod
    def from_name(cls, name):
        suffix = name.rsplit(".", 1)[-1]
        return cls._registry[suffix](name)


class ParquetFile(File):
    suffix = "parquet"


class JsonlFile(File):
    suffix = "jsonl"

class NdjsonFile(JsonlFile):
    # TODO: change ndjson to jsonl in gh extractor
    suffix = "ndjson"

# file_to_warehouse ----

@singledispatch
def file_to_warehouse(file_name, table_name):
    raise TypeError(f"Cannot handle type type `{type(tbl)}`")


@file_to_warehouse.register
def _ftw(file_name: str, table_name, *args, **kwargs):

    obj = File.from_name(file_name)
    if type(obj) is File:
        raise NotImplementedError(f"Cannot identify file type for file name: {file_name}")

    return file_to_warehouse(obj, table_name, *args, **kwargs)


@file_to_warehouse.register
def _ftw(file_name: ParquetFile, table_name):
    bucket = get_bucket()
    full_path = bucket + f"/{file_name.name}"

    sql = f"""SELECT * FROM read_parquet("{full_path}")"""

    copy_to_warehouse(sql, table_name)


@file_to_warehouse.register
def _ftw(file_name: JsonlFile, table_name):
    bucket = get_bucket()
    full_path = bucket + f"/{file_name.name}"

    sql = f"""SELECT * FROM read_json_objects("{full_path}")"""

    copy_to_warehouse(sql, table_name)

