from datetime import datetime
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator
from airflow.models import DAG
from airflow.utils.dates import days_ago

import os

SNOWFLAKE_SCHEMA = "STRAVA"
SNOWFLAKE_WAREHOUSE = "transforming"
SNOWFLAKE_DATABASE = "analytics"
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_CONN_ID = "snowflake_default"
S3_CONN_ID = "amazon_s3"
SNOWFLAKE_STAGE = "s3_stage"
AWS_KEY_ID = os.getenv("AWS_KEY")
AWS_SECRET = os.getenv("AWS_SECRET")
S3_URL = "s3://testedogabs/samsung health/samsunghealth_ghelleregear_20231027101980/"

SNOWFLAKE_SAMPLE_TABLE = "sleep_data"
# SNOWFLAKE_STAGE = "s3_stage"

FILE_PATH = "s3://testedogabs/samsung health/samsunghealth_ghelleregear_20231027101980/com.samsung.health.ecg.20231027101980.csv"

CREATE_STG_QUERY = f"""USE DATABASE ANALYTICS;
                     CREATE STAGE IF NOT EXISTS {SNOWFLAKE_STAGE}
                     URL ={S3_URL}
                     CREDENTIALS=(aws_key_id={AWS_KEY_ID}
                     aws_secret_key={AWS_SECRET})"""

default_args = {
    "owner": "airflow",
}

dag = DAG(
    "example_snowflake",
    default_args=default_args,
    start_date=days_ago(2),
    tags=["example"],
)

create_snowflake_stg = SnowflakeOperator(
    task_id="create_snowflake_stg",
    dag=dag,
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    sql=CREATE_STG_QUERY,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
)

copy_into_table = S3ToSnowflakeOperator(
    task_id="copy_into_table",
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    s3_keys=[FILE_PATH],
    table=SNOWFLAKE_SAMPLE_TABLE,
    schema=SNOWFLAKE_SCHEMA,
    stage=SNOWFLAKE_STAGE,
    file_format="(type = 'CSV',field_delimiter = ',')",
    dag=dag,
)

create_snowflake_stg >> copy_into_table
