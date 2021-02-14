import logging
import requests
from datetime import datetime, timedelta
import sys

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.base import BaseHook


class APItoPostgresOperator(BaseOperator):
    """
        Description: Custom operator that derives from BaseOperator.
                     This Operator is specific customized Operator
                     to get flight data from the OpenSky REST API
                     hour per hour and writes this data to postgres.

        Arguments:
            BaseOperator: Base class for all operators

        Returns:
            None
    """

    ui_color = '#358140'

    insert_sql = """
        INSERT INTO {}
        (icao24, firstSeen, estDepartureAirport, lastSeen, estArrivalAirport, callsign)
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}');
    """

    truncate_sql = """
        TRUNCATE TABLE {}
        RESTART IDENTITY;
    """


    @apply_defaults
    def __init__(self,
                 postgres_conn_id='',
                 table='',
                 api_path='',
                 api_conn_id='',
                 api_query_date='',
                 *args, **kwargs):

        super(APItoPostgresOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.table = table
        self.api_path = api_path
        self.api_conn_id = api_conn_id
        self.api_query_date = api_query_date

    def execute(self, context):
        """
        Description: This execution function gets flight data from the OpenSky REST API
                     hour per hour and writes this data to postgres.

        Arguments:
            self: Instance of the class
            context: Context dictionary

        Returns:
            None
        """

        # Build connections
        postgres = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        api_connection = BaseHook.get_connection(conn_id=self.api_conn_id)

        # Build correct timestamps in unix-format for passing to the api query
        self.log.info('api_query_dateeee: {}'.format(self.api_query_date.format(**context)))
        start_time = datetime.fromisoformat(self.api_query_date.format(**context))
        end_time = start_time + timedelta(hours=1)
        start_timestamp = str(int(datetime.timestamp(start_time)))
        end_timestamp = str(int(datetime.timestamp(end_time)))

        # Build complete api path
        # 'https://{}:{}@opensky-network.org/api/flights/all?begin={}&end={}'
        complete_api_path = self.api_path.format(api_connection.login, api_connection.password, start_timestamp, end_timestamp)
        self.log.info('api_path: {}'.format(complete_api_path))

        # Truncate table
        #self.log.info('Clearing data from Postgres staging table {}'.format(self.table))
        #trunc_formatted_sql = APItoPostgresOperator.truncate_sql.format(self.table)
        #postgres.run(trunc_formatted_sql)

        # Get data from api
        try:
            response = requests.get(complete_api_path)
            data = response.json()
        except:
            self.log.info('API request error - message:{}'.format(sys.exc_info()[0]))
        
        # If response is OK and length of data > 0 then write data to the database
        if(response.status_code == 200):
            if(len(data) > 0):
                for element in data:
                    formatted_sql = APItoPostgresOperator.insert_sql.format(self.table,
                                                                            element['icao24'],
                                                                            element['firstSeen'],
                                                                            element['estDepartureAirport'],
                                                                            element['lastSeen'],
                                                                            element['estArrivalAirport'],
                                                                            element['callsign']
                                                                            )
                    postgres.run(formatted_sql)
            else:
                self.log.info('API request doesnt contain data - datetime:{}'.format(start_time))

        else:
            self.log.info('API request problem - datetime:{} - response_code:{}'.format(start_time, str(response)))


        self.log.info('APItoPostgresOperator for {} completed - datetime: {}'.format(self.table, start_time))