import logging

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadFactOperator(BaseOperator):
    """
        Description: Custom operator that derives from BaseOperator.
                     This Operator is specific customized Operator
                     to fill a given fact table with a passed
                     SQL statement.

        Arguments:
            BaseOperator: Base class for all operators

        Returns:
            None
    """

    ui_color = '#80BD9E'
    
    insert_sql = """
        INSERT INTO {} 
        {};
    """
    
    @apply_defaults
    def __init__(self,
                 postgres_conn_id='',
                 table='',
                 insert_sql_query='',
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id=postgres_conn_id
        self.table=table
        self.insert_sql_query=insert_sql_query

    def execute(self, context):
        """
        Description: This custom function fills a given fact table with a passed
                     SQL statement.

        Arguments:
            self: Instance of the class
            context: Context dictionary

        Returns:
            None
        """

        # Build connection
        postgres = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        
        # Realize insert statement to fill dimension table
        formatted_sql = LoadFactOperator.insert_sql.format(self.table, self.insert_sql_query)
        postgres.run(formatted_sql)

        self.log.info('LoadFactOperator for dimension table {} completed'.format(self.table))