# ---
# python_callable: main
# op_kwargs:
#   owner: tidyverse
# python_callable_partials:
#   blob: {name: blob}
#   dbplyr: {name: dbplyr}
#   # design: {name: design}
#   # dplyr: {name: dplyr}
#   # dtplyr: {name: dtplyr}
#   # forcats: {name: forcats}
#   # funs: {name: funs}
#   # ggplot2: {name: ggplot2}
#   # ggplot2-docs: {name: ggplot2-docs}
#   # glue: {name: glue}
#   # googledrive: {name: googledrive}
#   # googlesheets4: {name: googlesheets4}
#   # haven: {name: haven}
#   # hms: {name: hms}
#   # lubridate: {name: lubridate}
#   # magrittr: {name: magrittr}
#   # modelr: {name: modelr}
#   # multidplyr: {name: multidplyr}
#   # nycflights13: {name: nycflights13}
#   # purrr: {name: purrr}
#   # readr: {name: readr}
#   # readxl: {name: readxl}
#   # reprex: {name: reprex}
#   # rvest: {name: rvest}
#   # stringr: {name: stringr}
#   # style: {name: style}
#   # tibble: {name: tibble}
#   # tidy-dev-day: {name: tidy-dev-day}
#   # tidyeval: {name: tidyeval}
#   # tidyr: {name: tidyr}
#   # tidytemplate: {name: tidytemplate}
#   # tidyups: {name: tidyups}
#   # tidyverse: {name: tidyverse}
#   # tidyverse.org: {name: tidyverse.org}
#   # tidyversedashboard: {name: tidyversedashboard}
#   # vroom: {name: vroom}
#   # website-analytics: {name: website-analytics}
# ---

import os

from gh_api.download import Downloader

def main(owner, name):
    
    downloader = Downloader("/usr/local/bucket/github_extract", api_key = os.environ["EXTRACTOR_GITHUB_TOKEN"])
    downloader.dump_repo(owner, name)
