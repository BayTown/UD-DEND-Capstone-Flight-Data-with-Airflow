import logging

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.postgres.hooks.postgres import PostgresHook

class CSVToPostgresOperator(BaseOperator):
    """
        Description: Custom operator that derives from BaseOperator.
                     This Operator loads data from a csv-file and writes it to postgres.

        Arguments:
            BaseOperator: Base class for all operators

        Returns:
            None
    """

    ui_color = '#c1ff33'

    copy_sql = """
        COPY {}
        FROM '{}'
        DELIMITER '{}'
        {};
    """

    truncate_sql = """
        TRUNCATE TABLE {}
        RESTART IDENTITY;
    """


    @apply_defaults
    def __init__(self,
                 postgres_conn_id='',
                 table='',
                 path_to_csv='',
                 delimiter=',',
                 additional_params='',
                 *args, **kwargs):

        super(CSVToPostgresOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id
        self.table = table
        self.path_to_csv = path_to_csv
        self.delimiter = delimiter
        self.additional_params=additional_params

    def execute(self, context):
        """
        Description: This execution function loads data from a
                     csv-file and writes it to postgres.

        Arguments:
            self: Instance of the class
            context: Context dictionary

        Returns:
            None
        """

        postgres = PostgresHook(postgres_conn_id=self.postgres_conn_id)

        # Truncate table
        self.log.info('Clearing data from Postgres staging table {}'.format(self.table))
        trunc_formatted_sql = CSVToPostgresOperator.truncate_sql.format(self.table)
        postgres.run(trunc_formatted_sql)

        # Copying data from CSV to Postgres
        self.log.info('Copying data from CSV to Postgres - {}'.format(self.table))
        formatted_sql = CSVToPostgresOperator.copy_sql.format(
            self.table,
            self.path_to_csv,
            self.delimiter,
            self.additional_params
        )
        postgres.run(formatted_sql)
        self.log.info('CSVToPostgresOperator for {} completed'.format(self.table))