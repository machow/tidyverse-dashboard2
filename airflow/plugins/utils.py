import os
import siuba as sb
import pandas as pd

from siuba.sql import LazyTbl
from functools import singledispatch, lru_cache
from sqlalchemy import create_engine


ENGINE_URI = "duckdb:///./data/_warehouse.duckdb"

def compile_sql(tbl: LazyTbl):
    sel = tbl.last_select
    compiled = sel.compile(
        dialect = tbl.source.dialect,
        compile_kwargs = {"literal_binds": True}
    )

    return str(compiled)


@lru_cache(maxsize=None)
def get_sql_engine():
    return create_engine(ENGINE_URI)


# copy_to_warehouse ===========================================================

@singledispatch
def copy_to_warehouse(tbl, name: str):
    raise TypeError(f"Cannot copy data of type `{type(data)}` to warehouse")


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
    print("YOOO")
    engine.execute(f"""DROP TABLE IF EXISTS "{name}" """)
    sql_tbl.create(name)
    

@copy_to_warehouse.register
def _ctw(tbl: str, name: str):
    create_stmt = f"""CREATE OR REPLACE TABLE "{name}" AS {tbl}"""

    engine = get_sql_engine()
    engine.execute(create_stmt)
