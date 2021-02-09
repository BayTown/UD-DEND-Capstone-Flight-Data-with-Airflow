import logging
import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import Mapping, PostgresOperator

from operators.APItoPostgresOperator import APItoPostgresOperator
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'ah',
    'depends_on_past': False,
    'start_date': datetime(2018, 1, 1, 0, 0, 0, 0),
    'end_date': datetime(2021, 2, 8, 0, 0, 0, 0),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}


dag = DAG("aa_dag_staging_flights", default_args=default_args, schedule_interval='@hourly', max_active_runs=1)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_flights_task = APItoPostgresOperator(
    task_id='stage_flights',
    dag=dag,
    postgres_conn_id='postgres',
    table='staging_flights',
    api_path='https://{}:{}@opensky-network.org/api/flights/all?begin={}&end={}',
    api_conn_id='openskynetwork',
    api_query_date='{execution_date}'
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >> stage_flights_task
stage_flights_task >> end_operator