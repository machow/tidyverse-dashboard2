# ---
# python_callable: main
# op_kwargs:
#   owner: tidyverse
#   #api_key: "{{ get_var('EXTRACTOR_GITHUB_TOKEN') }}"
# python_callable_partials:
#   blob: {name: blob}
#   dbplyr: {name: dbplyr}
#   design: {name: design}
#   dplyr: {name: dplyr}
#   dtplyr: {name: dtplyr}
#   forcats: {name: forcats}
#   funs: {name: funs}
#   ggplot2: {name: ggplot2}
#   ggplot2-docs: {name: ggplot2-docs}
#   glue: {name: glue}
#   googledrive: {name: googledrive}
#   googlesheets4: {name: googlesheets4}
#   haven: {name: haven}
#   hms: {name: hms}
#   lubridate: {name: lubridate}
#   magrittr: {name: magrittr}
#   modelr: {name: modelr}
#   multidplyr: {name: multidplyr}
#   nycflights13: {name: nycflights13}
#   purrr: {name: purrr}
#   readr: {name: readr}
#   readxl: {name: readxl}
#   reprex: {name: reprex}
#   rvest: {name: rvest}
#   stringr: {name: stringr}
#   style: {name: style}
#   tibble: {name: tibble}
#   tidy-dev-day: {name: tidy-dev-day}
#   tidyeval: {name: tidyeval}
#   tidyr: {name: tidyr}
#   tidytemplate: {name: tidytemplate}
#   tidyups: {name: tidyups}
#   tidyverse: {name: tidyverse}
#   tidyverse.org: {name: tidyverse.org}
#   tidyversedashboard: {name: tidyversedashboard}
#   vroom: {name: vroom}
#   website-analytics: {name: website-analytics}
# ---

import os
import tempfile
import pendulum 

from utils import previous_date


def main(owner, name, start=None, api_key=None):
    from gh_reader.download import Downloader
    import fsspec

    fs = fsspec.filesystem("gs")

    if start is None:
        start = previous_date()
   
    with tempfile.TemporaryDirectory() as tmp_dir:
        downloader = Downloader(
            tmp_dir,
            api_key = api_key
        )
        downloader.dump_repo(owner, name)

        dst_path = f"gs://tidyverse-pipeline/github_extract/dt={start}/{owner}+{name}"

        print(f"Saving to: {dst_path}")

        fs.put(
            f"{tmp_dir}/{owner}+{name}",
            dst_path,
            recursive=True
        )


if __name__ == "__main__":
    main("tidyverse", "blob", start = pendulum.now()) 
