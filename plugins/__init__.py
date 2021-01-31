from airflow.plugins_manager import AirflowPlugin

import operators

# Defining the plugin class
class FlightData(AirflowPlugin):
    name = "flightdata_plugin"
    operators = [
        operators.CSVToPostgresOperator,
        operators.DownloadCSVOperator
    ]
