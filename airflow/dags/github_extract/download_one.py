# ---
# python_callable: main
# ---

import os
import tempfile

from gh_api.download import Downloader

def main():
    with tempfile.TemporaryDirectory() as tmp:
        downloader = Downloader(tmp, api_key = os.environ["EXTRACTOR_GITHUB_TOKEN"])

        # this repo is very small, so hopefully fast to extract
        downloader.dump_repo("tidyverse", "tidytemplate")

