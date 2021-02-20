from datetime import datetime, timedelta
import logging
import os

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import Mapping, PostgresOperator
from operators.CSVToPostgresOperator import CSVToPostgresOperator
from operators.DownloadCSVOperator import DownloadCSVOperator
from operators.GetAirportsOperator import GetAirportsOperator
from operators.DataQualityOperator import DataQualityOperator
from operators.LoadDimensionOperator import LoadDimensionOperator
from airflow.operators.python import PythonOperator

from helpers.sqlstatements import SqlQueries

"""
Description:
# Get aircraft and airport data from the OpenSky Network
This DAG (Directed Acyclic Graph) builds a data pipeline
to get aircraft and airport data from the OpenSky Network

"""

# Path to a temporary folder where the CSV files can be temporarily saved.
temp_path = '/home/andi-ml/Documents/projects/UD-DEND-Capstone-Flight-Data-with-Airflow/tmp'

default_args = {
    'owner': 'ah',
    'start_date': datetime(2021, 2, 15, 0, 0, 0, 0),
    'end_date': datetime(2022, 1, 1, 0, 0, 0, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

dag = DAG("dag_etl_aircraft_data", default_args=default_args, schedule_interval='@weekly', max_active_runs=1)

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

get_airports_task = GetAirportsOperator(
    task_id='get_airports',
    dag=dag,
    csv_file_name='airports.csv',
    tmp_path=temp_path
)

stage_airports_task = CSVToPostgresOperator(
    task_id='stage_airports',
    dag=dag,
    postgres_conn_id='postgres',
    table='staging_airports',
    path_to_csv=os.path.join(temp_path, 'airports.csv'),
    delimiter=',',
    additional_params='CSV HEADER'
)

run_quality_checks_task = DataQualityOperator(
    task_id='run_data_quality_checks',
    dag=dag,
    postgres_conn_id='postgres',
    data_quality_checks=[
        {'sql_query': 'SELECT COUNT(*) FROM staging_aircraft_types WHERE designator IS NULL', 'expected_result': 0},
        {'sql_query': 'SELECT COUNT(*) FROM staging_aircraft_database WHERE icao24 IS NULL', 'expected_result': 0},
        {'sql_query': 'SELECT COUNT(*) FROM staging_airports WHERE icao IS NULL', 'expected_result': 0}
    ]
)

load_aircraft_dimension_table_task = LoadDimensionOperator(
    task_id='load_aircraft_dimension_table',
    dag=dag,
    postgres_conn_id='postgres',
    table='dim_aircrafts',
    insert_sql_query=SqlQueries.aircraft_data_insert,
    truncate_table=True
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >> download_aircraft_types_task
start_operator >> download_aircraft_database_task
start_operator >> get_airports_task
download_aircraft_types_task >> stage_aircraft_types_task
download_aircraft_database_task >> stage_aircraft_database_task
get_airports_task >> stage_airports_task
stage_aircraft_types_task >> run_quality_checks_task
stage_aircraft_database_task >> run_quality_checks_task
stage_airports_task >> run_quality_checks_task
run_quality_checks_task >> load_aircraft_dimension_table_task
load_aircraft_dimension_table_task >> end_operator