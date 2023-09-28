from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow import DAG



dag_parameters = {
    "0wner": "airflow",
    "start_date": datetime(2023, 2, 3),
    "catchup": False,
    "retries": 3,
}


def hello():
    print('hello')


with DAG(
    dag_id="hello",
    default_args=dag_parameters,
    description="test",
    tags=["hi"],
    schedule="@hourly",

) as dag:
    start_pipeline = EmptyOperator(task_id="start_pipeline")

    hello_airflow = PythonOperator(
        task_id="test",
        python_callable=hello,
        execution_timeout=timedelta(seconds=60)
    )


    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # Orchestration
    start_pipeline >> hello_airflow >> end_pipeline
