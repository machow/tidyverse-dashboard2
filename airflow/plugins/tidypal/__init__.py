import os

from functools import singledispatch, lru_cache
from pathlib import Path

def get_bucket():
    return os.environ["PIPELINE_BUCKET"]


def get_fs():
    import fsspec
    return fsspec.filesystem("file")


def get_sql_engine(read_only=False):
    from sqlalchemy import create_engine

    #db_path = os.environ["PIPELINE_WAREHOUSE_URI"]

    return create_engine(
        f"duckdb:///:memory:",
    )
