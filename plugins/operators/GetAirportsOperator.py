import requests
import os
import logging
from traffic.data import airports
import pandas as pd

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

class GetAirportsOperator(BaseOperator):
    ui_color = '#03e8fc'


    @apply_defaults
    def __init__(self,
                 csv_file_name,
                 tmp_path,
                 *args, **kwargs):

        super(GetAirportsOperator, self).__init__(*args, **kwargs)
        self.csv_file_name = csv_file_name
        self.tmp_path = tmp_path


    def execute(self, context):
        """
        Description: 

        Arguments:
            self: 
            context: 

        Returns:
            None
        """

        # Build path to csv
        csv_path = os.path.join(self.tmp_path, self.csv_file_name)
        # Download CSV-file from URL and save it to tmp path
        self.log.info('Get airport data from traffic api')
        airports.download_airports()
        airports.to_csv(csv_path)

        # Load csv to pandas dataframe and save it without index column
        df = pd.read_csv(csv_path, index_col=0)
        df.to_csv(csv_path, index=False)