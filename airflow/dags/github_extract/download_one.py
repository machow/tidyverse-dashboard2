# ---
# python_callable: main
# op_kwargs:
#   api_key: "{{ get_var('EXTRACTOR_GITHUB_TOKEN') }}"
# ---

import os
import tempfile

def main(api_key=None):
    from gh_reader.download import Downloader

    with tempfile.TemporaryDirectory() as tmp:
        downloader = Downloader(tmp, api_key = api_key)

        # this repo is very small, so hopefully fast to extract
        downloader.dump_repo("tidyverse", "tidytemplate")

