import logging
import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import Mapping, PostgresOperator

from operators.APItoPostgresOperator import APItoPostgresOperator
from operators.DataQualityOperator import DataQualityOperator
from operators.LoadFactOperator import LoadFactOperator
from operators.LoadDimensionOperator import LoadDimensionOperator
from airflow.operators.python import PythonOperator

from helpers.sqlstatements import SqlQueries


"""
Description:
# Get flight data from OpenSky REST API
This DAG (Directed Acyclic Graph) builds a data pipeline
to get flight data from OpenSky REST API.

"""


default_args = {
    'owner': 'ah',
    'depends_on_past': False,
    'start_date': datetime(2021, 2, 10, 2, 0, 0, 0),
    'end_date': datetime(2021, 2, 10, 3, 0, 0, 0),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}


dag = DAG("dag_etl_flight_data", default_args=default_args, schedule_interval='@hourly', max_active_runs=1)

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_flights_task = APItoPostgresOperator(
    task_id='stage_flights',
    dag=dag,
    postgres_conn_id='postgres',
    table='staging_flights',
    api_path='https://{}:{}@opensky-network.org/api/flights/all?begin={}&end={}',
    api_conn_id='openskynetwork',
    api_query_date='{execution_date}',
    truncate_table=True
)

run_quality_checks_task = DataQualityOperator(
    task_id='run_data_quality_checks',
    dag=dag,
    postgres_conn_id='postgres',
    data_quality_checks=[
        {'sql_query': 'SELECT COUNT(*) FROM staging_flights WHERE icao24 IS NULL', 'expected_result': 0}
    ]
)

load_flight_fact_table_task = LoadFactOperator(
    task_id='load_flight_fact_table',
    dag=dag,
    postgres_conn_id='postgres',
    table='fact_flights',
    insert_sql_query=SqlQueries.flight_data_insert
)

load_time_firstseen_dim_table_task = LoadDimensionOperator(
    task_id='load_time_firstseen_dim_table',
    dag=dag,
    postgres_conn_id='postgres',
    table='dim_time',
    insert_sql_query=SqlQueries.time_firstseen_insert,
    truncate_table=False
)

load_time_lastseen_dim_table_task = LoadDimensionOperator(
    task_id='load_time_lastseen_dim_table',
    dag=dag,
    postgres_conn_id='postgres',
    table='dim_time',
    insert_sql_query=SqlQueries.time_lastseen_insert,
    truncate_table=False
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >> stage_flights_task
stage_flights_task >> run_quality_checks_task
run_quality_checks_task >> load_flight_fact_table_task
load_flight_fact_table_task >> load_time_firstseen_dim_table_task
load_time_firstseen_dim_table_task >> load_time_lastseen_dim_table_task
load_time_lastseen_dim_table_task >> end_operator