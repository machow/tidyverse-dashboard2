EXAMPLE_FILES=tidypal/tests/example_files

$(EXAMPLE_FILES): scripts/create_example_data.py
	python $< $@

sync-gcs:
	gsutil rsync $(EXAMPLE_FILES) gs://tidyverse-dashboard/tests/$(EXAMPLE_FILES)
