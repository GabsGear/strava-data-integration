from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.utils.dates import days_ago

SNOWFLAKE_CONN_ID = 'snowflake_default'


SNOWFLAKE_SCHEMA = 'PUBLIC'
SNOWFLAKE_WAREHOUSE = 'transforming'
SNOWFLAKE_DATABASE = 'analytics'
SNOWFLAKE_SAMPLE_TABLE = 'teste'
S3_FILE_PATH = 'tabela.csv'

# SQL commands
CREATE_TABLE_SQL_STRING = (
    f"CREATE OR REPLACE TRANSIENT TABLE {SNOWFLAKE_SAMPLE_TABLE} (name VARCHAR(250), id INT);"
)
SQL_INSERT_STATEMENT = f"INSERT INTO {SNOWFLAKE_SAMPLE_TABLE} VALUES ('name', %(id)s)"
SQL_LIST = [SQL_INSERT_STATEMENT % {"id": n} for n in range(0, 10)]



default_args = {
    'owner': 'airflow',
}

dag = DAG(
    'example_snowflake',
    default_args=default_args,
    start_date=days_ago(2),
    tags=['example'],
)

snowflake_op_sql_str = SnowflakeOperator(
    task_id='snowflake_op_sql_str',
    dag=dag,
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    sql=CREATE_TABLE_SQL_STRING,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
)


snowflake_op_with_params = SnowflakeOperator(
    task_id='snowflake_op_with_params',
    dag=dag,
    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    sql=SQL_INSERT_STATEMENT,
    parameters={"id": 56},
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
)



snowflake_op_sql_str >> snowflake_op_with_params
