FROM jupyter/r-notebook:latest
#FROM python:3.9.1-slim-buster
USER root

# Postgres Requirements (For our Metadata Database)
RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN pip3 install psycopg2

# Install airflow and gusty
RUN pip3 install apache-airflow==2.3.3
RUN pip3 install gusty==0.16.0 siuba==0.4.2 duckdb_engine==0.6.8 pyarrow
RUN pip3 install git+https://github.com/machow/dbcooper-py.git@9a5eea3efa3693bcf82804a3313289c9b8550404
RUN pip3 install git+https://github.com/machow/gh_api.git@8e4ff69887bff58032014b0745eab4af8622a28a

# Airflow Env Vars
ENV AIRFLOW_HOME='/usr/local/airflow'

# Set wd
WORKDIR /usr/local/airflow

# Sleep forever
# CMD sleep infinity
