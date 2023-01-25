# ---
# ---

from utils import copy_to_warehouse

from siuba.data import mtcars

copy_to_warehouse(mtcars, "mtcars")
