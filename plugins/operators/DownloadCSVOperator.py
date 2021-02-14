import requests
import os
import logging

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

class DownloadCSVOperator(BaseOperator):
    """
        Description: Custom operator that derives from BaseOperator.
                     This Operator downloads csv-files.

        Arguments:
            BaseOperator: Base class for all operators

        Returns:
            None
    """

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
        Description: This execution function downloads a csv-file from a
                     given path and writes it to a local path.

        Arguments:
            self: Instance of the class
            context: Context dictionary

        Returns:
            None
        """

        # Download CSV-file from URL
        self.log.info('Download CSV-file {}'.format(self.csv_file_name))
        req = requests.get(self.csv_url)
        url_content = req.content

        # Save CSV-file to temporary path
        csv_path = os.path.join(self.tmp_path, self.csv_file_name)
        csv_file = open(csv_path, 'wb')
        csv_file.write(url_content)
        csv_file.close()