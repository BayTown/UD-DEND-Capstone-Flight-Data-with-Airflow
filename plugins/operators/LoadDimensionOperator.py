import logging

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadDimensionOperator(BaseOperator):
    """
        Description: Custom operator that derives from BaseOperator.
                     This Operator is specific customized Operator
                     to fill a given dimension table with a passed
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

    truncate_sql = """
        DELETE FROM {};
    """
    
    @apply_defaults
    def __init__(self,
                 postgres_conn_id='',
                 table='',
                 insert_sql_query='',
                 truncate_table=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id=postgres_conn_id
        self.table=table
        self.insert_sql_query=insert_sql_query
        self.truncate_table=truncate_table

    def execute(self, context):
        """
        Description: This custom function fills a given dimension table with a passed
                     SQL statement.

        Arguments:
            self: Instance of the class
            context: Context dictionary

        Returns:
            None
        """

        # Build connection
        postgres = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        
        # If parameter truncate_table is true, then truncate given table
        if self.truncate_table:
            self.log.info('Truncate data from dimension table {}'.format(self.table))
            trunc_formatted_sql = LoadDimensionOperator.truncate_sql.format(self.table)
            postgres.run(trunc_formatted_sql)
        
        # Realize insert statement to fill dimension table
        formatted_sql = LoadDimensionOperator.insert_sql.format(self.table, self.insert_sql_query)
        postgres.run(formatted_sql)

        self.log.info('LoadDimensionOperator for dimension table {} completed'.format(self.table))