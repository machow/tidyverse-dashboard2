import pytest
import pandas as pd

from pathlib import Path

from tidypal.utils import copy_to_warehouse


@pytest.mark.parametrize("tbl", [
    pd.DataFrame({"x": [1]}),
    "SELECT 1 AS x",
])
def test_copy_to_warehouse(tbl, backend):
    copy_to_warehouse(tbl, name="test_copy_to_warehouse", engine=backend.engine)


def test_copy_to_warehouse_diskhouse(diskhouse):
    df = pd.DataFrame({"x": [1,2,3]})
    copy_to_warehouse(df, "df", diskhouse)

    p_data = Path(diskhouse.dir_path) / "df.parquet"
    assert p_data.exists()

    res = pd.read_parquet(p_data)

    assert df.equals(res)


# def test_file_to_warehouse():
#     ...
