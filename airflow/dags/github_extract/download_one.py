# ---
# python_callable: main
# ---

import os
import tempfile

def main(api_key=None):
    from gh_reader.download import Downloader

    if api_key is None:
        # TODO: gusty now attempts to render top-matter like a jinja template at
        # operator *construction*, which means that we can't fetch variables
        # there anymore.
        from airflow.models import Variable

        api_key = Variable.get("EXTRACTOR_GITHUB_TOKEN")


    with tempfile.TemporaryDirectory() as tmp:
        downloader = Downloader(tmp, api_key = api_key)

        # this repo is very small, so hopefully fast to extract
        downloader.dump_repo("tidyverse", "tidytemplate")

