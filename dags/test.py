import datetime
import logging

from airflow import DAG
#from airflow.contrib.hooks.aws_hook import AwsHook
#from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import Mapping, PostgresOperator
from operators.CSVToPostgresOperator import CSVToPostgresOperator
from airflow.operators.python import PythonOperator



dag = DAG(
    "aa_testDAG_andi_ml",
    start_date=datetime.datetime.utcnow()
)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_aircraft_types_task = CSVToPostgresOperator(
    task_id='stage_aircraft_types',
    dag=dag,
    postgres_conn_id='postgres',
    table='staging_aircraft_types',
    path_to_csv='https://opensky-network.org/datasets/metadata/doc8643AircraftTypes.csv',
    delimiter=',',
    additional_params='CSV HEADER'
)




end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> stage_aircraft_types_task
stage_aircraft_types_task >> end_operator

# https://opensky-network.org/datasets/metadata/doc8643AircraftTypes.csv