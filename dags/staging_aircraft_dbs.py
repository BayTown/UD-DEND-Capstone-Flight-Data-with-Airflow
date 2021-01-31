import datetime
import logging
import os

from airflow import DAG
#from airflow.contrib.hooks.aws_hook import AwsHook
#from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import Mapping, PostgresOperator
from operators.CSVToPostgresOperator import CSVToPostgresOperator
from operators.DownloadCSVOperator import DownloadCSVOperator
from airflow.operators.python import PythonOperator

temp_path = '/home/andi-ml/Documents/projects/UD-DEND-Capstone-Flight-Data-with-Airflow/tmp'

dag = DAG(
    "aa_staging_aircraft_dbs",
    start_date=datetime.datetime.utcnow()
)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

download_aircraft_types_task = DownloadCSVOperator(
    task_id='download_aircraft_types',
    dag=dag,
    csv_url='https://opensky-network.org/datasets/metadata/doc8643AircraftTypes.csv',
    csv_file_name='AircraftTypes.csv',
    tmp_path=temp_path
)

stage_aircraft_types_task = CSVToPostgresOperator(
    task_id='stage_aircraft_types',
    dag=dag,
    postgres_conn_id='postgres',
    table='staging_aircraft_types',
    path_to_csv=os.path.join(temp_path, 'AircraftTypes.csv'),
    delimiter=',',
    additional_params='CSV HEADER'
)

download_manufacturers_task = DownloadCSVOperator(
    task_id='download_manufacturers',
    dag=dag,
    csv_url='https://opensky-network.org/datasets/metadata/doc8643Manufacturers.csv',
    csv_file_name='Manufacturers.csv',
    tmp_path=temp_path
)

stage_manufacturers_task = CSVToPostgresOperator(
    task_id='stage_manufacturers',
    dag=dag,
    postgres_conn_id='postgres',
    table='staging_manufacturers',
    path_to_csv=os.path.join(temp_path, 'Manufacturers.csv'),
    delimiter=',',
    additional_params='CSV HEADER'
)

download_aircraft_database_task = DownloadCSVOperator(
    task_id='download_aircraft_database',
    dag=dag,
    csv_url='https://opensky-network.org/datasets/metadata/aircraftDatabase.csv',
    csv_file_name='aircraftDatabase.csv',
    tmp_path=temp_path
)

stage_aircraft_database_task = CSVToPostgresOperator(
    task_id='stage_aircraft_database',
    dag=dag,
    postgres_conn_id='postgres',
    table='staging_aircraft_database',
    path_to_csv=os.path.join(temp_path, 'aircraftDatabase.csv'),
    delimiter=',',
    additional_params='CSV HEADER'
)



end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> download_aircraft_types_task
start_operator >> download_manufacturers_task
start_operator >> download_aircraft_database_task
download_aircraft_types_task >> stage_aircraft_types_task
download_manufacturers_task >> stage_manufacturers_task
download_aircraft_database_task >> stage_aircraft_database_task
stage_aircraft_types_task >> end_operator
stage_manufacturers_task >> end_operator
stage_aircraft_database_task >> end_operator