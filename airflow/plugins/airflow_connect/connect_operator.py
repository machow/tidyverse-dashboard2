import os

from airflow.models import BaseOperator
from airflow_connect import api
from pins.rsconnect.fs import RsConnectFs

class ConnectOperator(BaseOperator):

    def __init__(
        self,
        file_path,
        **kwargs
    ):
        self.file_path = file_path
        super().__init__(**kwargs)

    def execute(self, context):
        # TODO: pins should automatically look for this variable
        fs = RsConnectFs(os.environ["CONNECT_SERVER"])
        api.trigger_deploy_or_rerun(fs, self.file_path)
