import requests
import os
import logging

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

class DownloadCSVOperator(BaseOperator):
    ui_color = '#03e8fc'


    @apply_defaults
    def __init__(self,
                 csv_url, 
                 csv_file_name,
                 tmp_path,
                 *args, **kwargs):

        super(DownloadCSVOperator, self).__init__(*args, **kwargs)
        self.csv_url = csv_url
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

        # Download CSV-file from URL
        self.log.info('Download CSV-file {}'.format(self.csv_file_name))
        req = requests.get(self.csv_url)
        url_content = req.content

        # Save CSV-file to temporary path
        complete_path = os.path.join(self.tmp_path, self.csv_file_name)
        csv_file = open(complete_path, 'wb')
        csv_file.write(url_content)
        csv_file.close()