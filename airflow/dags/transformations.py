from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping
from airflow.utils.dates import days_ago


SNOWFLAKE_SCHEMA = 'STRAVA'
SNOWFLAKE_DATABASE = 'analytics'

DBT_PROJECT_FOLDER = "airflow/dags/dbt/activities_data_integration"


profile_config = ProfileConfig(
    profile_name="activities_data_integration",
    target_name="dev",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snowflake_default",
        profile_args={
            "database": SNOWFLAKE_DATABASE,
            "schema": SNOWFLAKE_SCHEMA,
        },
    ),
)


activities_transform = DbtDag(
    project_config=ProjectConfig(
        DBT_PROJECT_FOLDER,
    ),
    profile_config=profile_config,
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
    dag_id="activities_transformations",
    tags=["transformations"],
)
