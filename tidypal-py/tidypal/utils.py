import os
import logging
import siuba as sb
import pandas as pd

from dataclasses import dataclass
from plum import dispatch, type_of
from pathlib import Path
from siuba.sql import LazyTbl
from sqlalchemy import create_engine
from typing import Union

from tidypal.config import get_sql_engine, get_bucket
from tidypal import data as dc


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


def fully_qualified_name(name: str, engine: dc.SqlEngine, escape=True):
    # TODO: is there a way to just do all this via an engine method, etc..?
    max_parts = 3
    parts = name.split(".")

    if len(parts) > max_parts:
        raise ValueError(f"Table has too many parts: {len(parts)}")

    name, schema, database = reversed(parts) + [None]*(max_parts - len(parts))

    defaults = extract_table_name_defaults(engine)

    if schema is None:
        if defaults["schema"] is None:
            raise ValueError("No database schema specified, and no schema set for the engine.")
        schema = defaults["schema"]
    if database is None:
        if defaults["database"] is None:
            raise ValueError("No database database name specified, and no schema set for the engine.")
        database = defaults["database"]

    # TODO: the ` character is bigquery specific
    if escape:
        return f"`{database}`.`{schema}`.`{name}`"

    return f"{database}.{schema}.{name}"


@dispatch
def extract_table_name_defaults(engine: dc.SqlEngine):
    return {"database": engine.host, "schema": engine.database}


# copy_to_warehouse ===========================================================

#@dispatch
#def copy_to_warehouse(tbl, name, engine):
#    raise TypeError(f"Cannot copy data of type `{type(tbl)}` to warehouse")


@dispatch
def copy_to_warehouse(tbl, name, engine: None = None, **kwargs):
    if engine is None:
        engine = get_sql_engine()

    copy_to_warehouse(tbl, name, engine=engine, **kwargs)


@dispatch
def copy_to_warehouse(tbl: LazyTbl, name: str, engine: dc.SqlEngineDuckdb):
    compiled = compile_sql(data)

    create_stmt = f"""CREATE OR REPLACE TABLE "{name}" AS {compiled}"""

    engine.execute(create_stmt)
    

@dispatch
def copy_to_warehouse(tbl: pd.DataFrame, name: str, engine: dc.SqlEngineDuckdb):

    sql_tbl = engine.connect().connection.c.from_df(tbl)

    # note that duckdbs create method can't replace :/
    engine.execute(f"""DROP TABLE IF EXISTS "{name}" """)
    sql_tbl.create(name)
    

@dispatch
def copy_to_warehouse(tbl: pd.DataFrame, name: str, engine: dc.SqlEngine, if_exists = "replace"):

    # Note that pandas gbq does not allow quoted name parts (with `)
    # e.g. `my-project`.`my-dataset`.`a-table`
    full_name = fully_qualified_name(name, engine, escape=False)
    tbl.to_gbq(full_name, if_exists=if_exists)


@dispatch
def copy_to_warehouse(tbl: str, name: str, engine: dc.SqlEngine):

    # TODO: use something like dbcooper-py generic dispatch use name for dispatch
    create_stmt = SQL_TEMPLATE.format(sql=tbl, name=name)

    logging.info(create_stmt)

    engine.execute(create_stmt)


@dispatch
def copy_to_warehouse(tbl: Union[str, pd.DataFrame], name: str, engine: dc.DuckdbDiskhouse):
    # just create parquet files on disk
    sql = tbl if isinstance(tbl, str) else "SELECT * FROM tbl"

    sql_engine = engine.engine
    warehouse_path = engine.dir_path

    Path(warehouse_path).mkdir(exist_ok=True)

    # TODO: support formats other than parquet
    final_name = warehouse_path + "/" + name
    create_stmt = SQL_DUCKDB_TEMPLATE.format(sql=sql, name = final_name)

    logging.info(create_stmt)

    sql_engine.execute(create_stmt)


# File to warehouse ===========================================================

# file_to_warehouse ----

from functools import singledispatch

@singledispatch
def file_to_warehouse(file_name, table_name):
    raise TypeError(f"Cannot handle type type `{type(tbl)}`")


@file_to_warehouse.register
def _ftw(file_name: str, table_name, *args, **kwargs):

    obj = dc.File.from_name(file_name)
    if type(obj) is dc.File:
        raise NotImplementedError(f"Cannot identify file type for file name: {file_name}")

    return file_to_warehouse(obj, table_name, *args, **kwargs)


@file_to_warehouse.register
def _ftw(file_name: dc.ParquetFile, table_name):
    bucket = get_bucket()
    full_path = bucket + f"/{file_name.name}"

    sql = f"""SELECT * FROM read_parquet("{full_path}")"""

    copy_to_warehouse(sql, table_name)


@file_to_warehouse.register
def _ftw(file_name: dc.JsonlFile, table_name):
    bucket = get_bucket()
    full_path = bucket + f"/{file_name.name}"

    sql = f"""SELECT * FROM read_json_objects("{full_path}")"""

    copy_to_warehouse(sql, table_name)

