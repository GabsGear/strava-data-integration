from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping

from airflow import DAG


from datetime import datetime
import os

profile_config = ProfileConfig(
    profile_name="activities_data_integration",
    target_name="dev",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snowflake_default",
        profile_args={
            "database": "ANALYTICS",
            "schema": "STRAVA",
        },
    ),
)

my_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        "airflow/dags/dbt/activities_data_integration",
    ),
    profile_config=profile_config,
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dag_id="activities_transformations",
)

my_cosmos_dag
