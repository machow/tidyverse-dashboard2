from tidypal.data import Duckdb, Bigquery, SqlEngine
from sqlalchemy.engine import Engine
from plum import dispatch, type_of
from sqlalchemy import create_engine


@dispatch
def f(engine: SqlEngine[Duckdb]):
    print("doing stuff")
    return 1

def test_dispatch_abc():
    engine = create_engine("duckdb:///:memory:")
    res = f(engine)
    assert res == 1
