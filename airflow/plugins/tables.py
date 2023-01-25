from dbcooper import DbCooper, AccessorBuilder
from functools import lru_cache
import utils

@lru_cache(maxsize=None)
def get_dbc():
    engine = utils.get_sql_engine()
    return DbCooper(
        engine,
        accessor_builder = AccessorBuilder(format_from_part="table")
    )
