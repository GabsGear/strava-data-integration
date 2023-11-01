import os

import requests
import snowflake.connector as snow
import urllib3
from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from pandas.io.json import json_normalize
from snowflake.connector.pandas_tools import write_pandas
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import timedelta

SNOWFLAKE_SCHEMA = "STRAVA"
SNOWFLAKE_WAREHOUSE = "transforming"
SNOWFLAKE_DATABASE = "analytics"
SNOWFLAKE_OUTPUT_TABLE = "raw_strava_activities"
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")

STRAVA_AUTH_URL = "https://www.strava.com/oauth/token"
STRAVA_ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"

TASK_EXECUTION_TIMEOUT_SECONDS = 60 * 5

snowflake_connection = BaseHook.get_connection("snowflake_default")


def create_snowflake_python_connm():
    return snow.connect(
        user=snowflake_connection.login,
        password=snowflake_connection.password,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )


def extract_strava_data():
    MAX_PAGES = 100
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    auth_url = STRAVA_AUTH_URL
    activites_url = STRAVA_ACTIVITIES_URL

    payload = {
        "client_id": os.getenv("STRAVA_CLIENT_ID"),
        "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
        "refresh_token": os.getenv("STRAVA_REFRESH_TOKEN"),
        "grant_type": "refresh_token",
        "f": "json",
    }

    res = requests.post(auth_url, data=payload, verify=False)
    my_dataset = []
    for page in range(1, MAX_PAGES + 1):
        response = requests.get(
            activites_url,
            headers={"Authorization": "Bearer " + res.json()["access_token"]},
            params={"per_page": 200, "page": page},
        ).json()
        if len(response) == 0:
            break
        my_dataset += response

    activities = json_normalize(my_dataset)
    activities.columns = map(lambda x: str(x).upper(), activities.columns)
    return activities


def load_pandas_data_fo_snowflake():
    conn = create_snowflake_python_connm()
    cur = conn.cursor()
    total = extract_strava_data()
    write_pandas(
        conn, total, SNOWFLAKE_OUTPUT_TABLE, auto_create_table=True, overwrite=True
    )
    cur = conn.cursor()
    cur.close()
    conn.close()


default_args = {
    "owner": "airflow",
}

dag = DAG(
    "create_raw_tables",
    default_args=default_args,
    start_date=days_ago(1),
    tags=["datafeeds"],
)

load_raw_data = PythonOperator(
    task_id="create_raw_data", dag=dag, python_callable=load_pandas_data_fo_snowflake
)

trigger_load_s3_to_snowflake = TriggerDagRunOperator(
    trigger_dag_id="s3_to_snowflake",
    task_id="trigger_s3_to_snowflake",
    execution_timeout=timedelta(seconds=TASK_EXECUTION_TIMEOUT_SECONDS),
)


trigger_dbt_transformations = TriggerDagRunOperator(
    trigger_dag_id="activities_transformations",
    task_id="trigger_dbt_transformations",
    execution_timeout=timedelta(seconds=TASK_EXECUTION_TIMEOUT_SECONDS),
)


[load_raw_data, trigger_load_s3_to_snowflake] >> trigger_dbt_transformations
