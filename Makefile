AIRFLOW_BUCKET=gs://us-central1-airflow-0851bd3e-bucket

update-requirements:
	gcloud composer environments update \
		airflow \
		--update-pypi-packages-from-file airflow/requirements.txt \
		--location us-central1 \
		--project tidyverse-pipeline

sync-config:
	gsutil rsync -r scripts/config $(AIRFLOW_BUCKET)/config

list-packages:
	gcloud beta composer environments list-packages \
		airflow \
		--location us-central1

update-packages:
	gcloud composer environments update airflow \
        --location us-central1 \
         --update-pypi-packages-from-file requirements-gcp.txt

update-dags:
	gsutil -m rsync -rdc -x "__pycache__" airflow/dags $(AIRFLOW_BUCKET)/dags

update-plugins:
	gsutil -m rsync -rdc -x "__pycache__" airflow/plugins $(AIRFLOW_BUCKET)/plugins
