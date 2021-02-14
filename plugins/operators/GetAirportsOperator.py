import requests
import os
import logging
from traffic.data import airports
import pandas as pd

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

class GetAirportsOperator(BaseOperator):
    """
        Description: Custom operator that derives from BaseOperator.
                     This Operator gets airport data form an api and writes it to csv.

        Arguments:
            BaseOperator: Base class for all operators

        Returns:
            None
    """

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
        Description: This execution function loads the airports from the traffic api
                     and writes it to csv

        Arguments:
            self: Instance of the class
            context: Context dictionary

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