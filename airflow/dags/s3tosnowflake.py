from datetime import datetime
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import DAG
from airflow.utils.dates import days_ago
import os
import snowflake.connector as snow
from airflow.hooks.base_hook import BaseHook


SNOWFLAKE_SCHEMA = "SAMSUNG"
SNOWFLAKE_WAREHOUSE = "transforming"
SNOWFLAKE_DATABASE = "analytics"
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_CONN_ID = "snowflake_default"
S3_CONN_ID = "amazon_s3"
SNOWFLAKE_STAGE = "s3_samsung_health_data"
AWS_KEY_ID = os.getenv("AWS_KEY")
AWS_SECRET = os.getenv("AWS_SECRET")
S3_URL = "s3://samsung-health-data/"
snowflake_connection = BaseHook.get_connection("snowflake_default")

CREATE_STG_QUERY = f"""
                     USE DATABASE ANALYTICS;
                     USE SCHEMA {SNOWFLAKE_SCHEMA};
                     CREATE STAGE IF NOT EXISTS {SNOWFLAKE_STAGE}
                     URL ={S3_URL}
                     CREDENTIALS=(aws_key_id='{AWS_KEY_ID}'
                     aws_secret_key='{AWS_SECRET}')
                     """

COPY_FROM_STAGE_QUERY = """
        CREATE OR REPLACE FILE FORMAT my_parquet_format TYPE = parquet;

        CREATE TABLE IF NOT EXISTS {table_name} 
        USING TEMPLATE (
            SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
            FROM TABLE(
                INFER_SCHEMA(
                LOCATION=>'@s3_samsung_health_data/calories_burned.parquet',
                FILE_FORMAT=>'my_parquet_format'
                )
            ));

        COPY INTO {table_name} 
        FROM @s3_samsung_health_data/{table_name}.parquet
            FILE_FORMAT = (FORMAT_NAME= 'my_parquet_format') 
            MATCH_BY_COLUMN_NAME=CASE_INSENSITIVE;
"""

table_list = [
    'breathing',
    'max_heart_rate',
    'pedometer_step_count',
    'report',
    'sleep',
    'friends',
    'food_frequent',
    'weight',
    'histogram',
    'preferences',
    'leaderboard',
    'food_info',
    'device_profile',
    'oxygen_saturation',
    'nutrition',
    'sleep_combined',
    'history',
    'exercise',
    'heart_rate',
    'service_status',
    'ecg',
    'badge',
    'extra',
    'rewards',
    'sleep_stage',
    'stress',
    'public_challenge',
    'floors_climbed',
    'details',
    'food_intake',
    'recovery_heart_rate',
    'user_profile',
    'height',
    'photo',
    'weather',
    'step_daily_trend',
    'pedometer_day_summary',
    'best_records',
    'day_summary',
    'food_favorite',
]

default_args = {
    "owner": "airflow",
}


with DAG(dag_id="s3_to_snowflake", start_date=days_ago(2), tags=["snowflake", "s3"]) as dag:
    create_snowflake_stg = SnowflakeOperator(
        task_id="create_snowflake_stg",
        dag=dag,
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
        sql=CREATE_STG_QUERY,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )
    with TaskGroup("create_tables", tooltip="Tasks for section_1") as create_tables_tg:
        for table in table_list:
            create_tables_from_stg = SnowflakeOperator(
                task_id=f"create_snowflake_tables_from_stage_{table}",
                dag=dag,
                snowflake_conn_id=SNOWFLAKE_CONN_ID,
                sql=COPY_FROM_STAGE_QUERY.format(table_name=table),
                warehouse=SNOWFLAKE_WAREHOUSE,
                database=SNOWFLAKE_DATABASE,
                schema=SNOWFLAKE_SCHEMA,
                ) 

create_snowflake_stg >> create_tables_tg