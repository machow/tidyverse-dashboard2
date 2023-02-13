#from airflow.models import BaseOperator
#from tidypal import get_fs
#
## for duckdb, this will just query parquet back to parquet
#class FileToWarehouseOperator(BaseOperator):
#
#    def __init__(
#        self,
#        file_name: str,
#        dst_table_name,
#        fields=None,
#    ):
#        self.file_name = file_name
#        self.dst_table_name = dst_table_name
#
#        if fields is not None:
#            raise NotImplementedError()
#
#    def execute(self, context):
#        fs = get_fs()
#        fs.
#        pass
#
