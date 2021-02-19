import logging

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """
        Description: Custom operator that derives from BaseOperator.
                     This Operator is specific customized Operator
                     to realize data quality checks with given SQL commands.

        Arguments:
            BaseOperator: Base class for all operators

        Returns:
            None
    """

    ui_color = '#33b2ff'

    @apply_defaults
    def __init__(self,
                 postgres_conn_id='',
                 data_quality_checks=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id=postgres_conn_id
        self.data_quality_checks=data_quality_checks

    def execute(self, context):
        """
        Description: This custom function implements one or more data quality checks that are passed as
                     SQL commands in the data_quality_checks list, executes them and checks the
                     return value for correctness. If everything fits, this function works without any problems.
                     If there is a disagreement, an error is thrown.

        Arguments:
            self: Instance of the class
            context: Context dictionary

        Returns:
            None
        """

        # Build connection
        postgres = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        
        # If no quality checks were specified, the function is terminated
        if len(self.data_quality_checks) <= 0:
            self.log.info('No data quality checks were specified. Data quality checks canceled.')
            return
        
        # Here every single quality check is run through, the associated SQL command is executed and the return value is checked.
        for check in self.data_quality_checks:
            sql_query = check.get('sql_query')
            expected_result = check.get('expected_result')
            
            try:
                self.log.info('Starting SQL query for data check - {}'.format(sql_query))
                records = postgres.get_records(sql_query)
                num_records = records[0][0]

                if num_records != expected_result:
                    raise ValueError('Data quality check failed. {} entries excpected. {} given'.format(expected_result, num_records))
                else:
                    self.log.info('Data Check passed for query - {}. Result: {}'.format(sql_query, num_records))
                    
            except ValueError as v:
                self.log.info(v.args)
                raise
            except Exception as e:
                self.log.info('SQL query for data check failed - {}. Exception: {}'.format(sql_query, e))
                raise