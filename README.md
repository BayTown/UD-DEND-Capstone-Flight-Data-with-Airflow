# Udacity Data Engineering Nanodegree - Project 6/6
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=flat-square&logo=python)](https://www.python.org/)
[![made-with-apache-airflow](https://img.shields.io/badge/Made%20with-Apache%20Airflow-blue.svg?logo=apache-airflow)](https://airflow.apache.org/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square&logo=appveyor)](https://lbesson.mit-license.org/)

## Capstone Project - Flight Data with Airflow


## Introduction  

This project is about historical flight data. It is about extracting historical flight data (facts)
and additional information (dimensions) from various sources, transforming them and loading them into a structured
data warehouse in order to make this data available for data analysis.  
If the project is successfully implemented, you should be able to search through the data warehouse, e.g. when at which airport which aircraft took off. Or how many aircraft have flown to a specific airport on a specific day.


## Project Description

In this project I extracted the required data from two different data sources (OpenSky Network and Python traffic API), then put them into a meaningful context using transform and then finally loaded the data into a database in the form of fact and dimension tables.  
When it comes to data sources, the OpenSource and OpenData concept was very important to me, as I believe that this will be the driver for our future world. Even if, as I will explain below, I had to accept a few flaws.  

I chose Apache Airflow and PostgreSQL as the technological basis to realize this project.

- [Apache Airflow](https://airflow.apache.org/)  
Apache Airflow is an open-source workflow management platform. Airflow allows to programmatically author and schedule their workflows and monitor them via the built-in Airflow user interface. Airflow is written in Python, and workflows are created via Python scripts. Airflow is designed under the principle of "configuration as code".

- [PostgreSQL](https://www.postgresql.org/)  
PostgreSQL also known as Postgres, is a free and open-source relational database management system (RDBMS) emphasizing extensibility and SQL compliance.

In this project I will use Apache Airflow to cyclically extract the data from the required data sources. And Postgres to load this transformed data into the database. This then functions as a data warehouse.

## Requirements

This project was done on a Linux-OS ([Ubuntu 20.04 LTS](https://ubuntu.com/download/desktop)) with the awesome open source code editor [Visual Studio Code](https://code.visualstudio.com/).

To implement the project you will need the following things:

- [Python](https://www.python.org/) Version 3.8.5
- [Apache Airflow](https://airflow.apache.org/) Version 2.0.0
- [PostgreSQL](https://www.postgresql.org/) Version 12.5

After you have installed Apache Airflow you have to create the connections for the OpenSky Network and for the Postgres database under Admin-> Connections. In my project these are implemented as the connection IDs `postgres` and `openskynetwork`.  
Also you have to create all the tables via the CREATE statements which are in the file `create_table_statements.sql`.

## Project Datasets - Data Sources

I extracted the following data from the OpenSky Network:
- aircraftDatabase (CSV-Format)
- aircraftTypes (CSV-Format)  
You can find them [here](https://opensky-network.org/datasets/metadata/)
- Flight Data (REST API)  
The problem that there is currently still is that there are often no entries at the departure airport and the arrival airport, since these data on the flight position values ​​are only estimated and. However, this deficiency did not prevent me from doing this project, because I want to show what is possible with open source data.  
A documentation about this flight data you can find [here](https://opensky-network.org/apidoc/rest.html#id6)


> The OpenSky Network, http://www.opensky-network.org  
>Bringing up OpenSky: A large-scale ADS-B sensor network for research 
>Matthias Schäfer, Martin Strohmeier, Vincent Lenders, Ivan Martinovic, Matthias Wilhelm
>ACM/IEEE International Conference on Information Processing in Sensor Networks, April 2014

And I extracted the following data from the Python traffic API:
- Airport data (Python API)

> [traffic](https://traffic-viz.github.io/index.html) – Air traffic data processing in Python  
> The traffic library helps working with common sources of air traffic data.  
> <cite>Xavier Olive</cite>  


## ETL pipeline

Here you can see an architecture diagram of the ETL pipeline:  
![ETL_Architecture](https://user-images.githubusercontent.com/32474126/108607653-eb63ca00-73c1-11eb-92ef-6ab3011a400a.png)

There are two DAGs that implement the ETL pipeline for this project. I want to explain these in more detail here:
- dag_etl_aircraft_data  
  This DAG implements the extract of the csv files `aircraftDatabase.csv` and` AircraftTypes.csv` and the airport data via the traffic API and loads them into the respective staging tables. Then these are transferred and loaded into the dimension tables `dim_aircrafts` and `dim_airports`.  
  I have chosen once a week `@weekly` as the cycle for this DAG because that type of master data is completely sufficient for this.
  ![graph_view_dag_etl_aricraft_data](https://user-images.githubusercontent.com/32474126/108609066-b197c100-73cb-11eb-836a-4b83b4dcfa99.png)

- dag_etl_flight_data  
  In this DAG the flight data of the OpenSky Network REST API are retrieved. The connection string is as follows:  
  `'https://{USERNAME}:{PASSWORD}@opensky-network.org/api/flights/all?begin={UNIXTIMESTAMP Start of the time interval}&end={UNIXTIMESTAMP End of the time interval}'`  
  A documentation about this you can find [here](https://opensky-network.org/apidoc/rest.html#flights-in-time-interval)  
  For this purpose, the DAG transfers the `execution_date` to the `APIToPostgresOperator`, which converts the datetime timestamp into a UNIX timestamp. This represents the starttime `begin`. An hour is added to the endtime. This means that for each query or each execution of the DAG, one hour is queried as a period to the API.  
  Therefore the cycle for this DAG is one hour `@hourly`.
  As part of this project, all flight data between 01.01.2018 and 10.02.2021 were requested. That is 1136 days or 27264 hours and thus 27264 requests to the API.
  ![graph_view_dag_etl_flight_data](https://user-images.githubusercontent.com/32474126/108608300-6b8c2e80-73c6-11eb-8592-b1b0af6b64fb.png)


### Data Quality Checks
The following data quality checks are carried out:
- In the table `staging_aircraft_types`, the column `designator` is checked for NULL values
- In the table `staging_aircraft_database`, the column `icao24` is checked for NULL values
- In the table `staging_airports`, the column `icao` is checked for NULL values
- In the table `staging_flights`, the column `icao24` is checked for NULL values


## Database schema
Here you can take a view of the final data model:  
![ERD_final_data_model](https://user-images.githubusercontent.com/32474126/108609629-78615000-73cf-11eb-91d7-9ad2363420b2.png)

Amounts of data entries (21.01.2021):  
| Table         | Entries    |
|---------------|------------|
| dim_aircrafts | 460,000    |
| dim_time      | 29,161,422 |
| dim_airports  | 62,301     |
| fact_flights  | 18,363,826 |
  

### Data dictionary of the final data model
  
#### Table dim_aircrafts  

This table contains all aircraft with the most relevant data about the aircrafts: 
| Attribute           | Datatype | Description                                                                                 | Example   |
|---------------------|----------|---------------------------------------------------------------------------------------------|-----------|
| icao24              | TEXT     | Unique ICAO 24-bit address of the transponder of the aircraft                               | 3c4a8b    |
| registration        | TEXT     | Aircraft registration code, alternatively called tail number                                | D-ABTK    |
| operator            | TEXT     | Operator of the aircraft                                                                    | Lufthansa |
| operatoricao        | TEXT     | The ICAO airline designator is a code assigned by the (ICAO) to aircraft operating agencies | DLH       |
| owner               | TEXT     | Owner of the aircraft                                                                       | Lufthansa |
| manufacturericao    | TEXT     | ICAO manufacturer designator                                                                | BOEING    |
| manufacturername    | TEXT     | Name of the aircraft manufacturer                                                           | Boeing    |
| typecode            | TEXT     | Short type code of the aircraft model                                                       | B744      |
| model               | TEXT     | Aircraft model                                                                              | 747 430   |
| serialnumber        | TEXT     | Aircraft serial number                                                                      | 29871     |
| aircraftdescription | TEXT     | Parent aircraft type                                                                        | LandPlane |
| wtc                 | TEXT     | ICAO Wake Turbulence Category (J, H, M, L)                                                  | H         |
| enginetype          | TEXT     | Type of engines                                                                             | Jet       |
| enginecount         | INTEGER  | Number of engines                                                                           | 4         |
  
#### Table dim_time
All time stamps with the associated time units are in this table in order to enable faster queries in relation to the fact table:  
| Attribute | Datatype | Description                      | Example             |
|-----------|----------|----------------------------------|---------------------|
| seen_time | DATETIME | Datetime Timestamp               | 2018-01-01 00:00:03 |
| hour      | INTEGER  | Hour in relation to seen_time    | 0                   |
| day       | INTEGER  | Day in relation to seen_time     | 1                   |
| week      | INTEGER  | Week in relation to seen_time    | 1                   |
| month     | INTEGER  | Month in relation to seen_time   | 1                   |
| year      | INTEGER  | Year in relation to seen_time    | 2018                |
| weekday   | INTEGER  | Weekday in relation to seen_time | 1                   |

#### Table dim_airports
This table contains all airports with the most important relevant data:  
| Attribute    | Datatype | Description                            | Example        |
|--------------|----------|----------------------------------------|----------------|
| icao         | TEXT     | ICAO code of the airport               | EDDM           |
| name         | TEXT     | Name of the Airport                    | Munich Airport |
| iata         | TEXT     | IATA code of the airport               | MUC            |
| latitude     | NUMERIC  | Geographical latitude of the airport   | 48             |
| longitude    | NUMERIC  | Longitude of the airport geographical  | 12             |
| country      | TEXT     | Country of the airport                 | Germany        |
| altitude     | NUMERIC  | Altitude of the airport in feet        | 1487           |
| type         | TEXT     | Airport size type                      | large_airport  |
| municipality | TEXT     | Municipality of the airport            | Munich         |

#### Table fact_flights
This table contains all flights with the most relevant values:

| Attribute           | Datatype | Description                                                                           | Example                          |
|---------------------|----------|---------------------------------------------------------------------------------------|----------------------------------|
| flight_id           | TEXT     | MD5 hash formed from the values icao24 and firstSeenTime of the table staging_flights | 0000a96b470e06ffa3312b39fee2ecb2 |
| icao24              | TEXT     | Unique ICAO 24-bit address of the transponder of the aircraft                         | 3006b5                           |
| firstSeenTime       | DATETIME | Estimated time of departure for the flight as Unix time (seconds since epoch)         | 2018-06-24 06:19:30              |
| estDepartureAirport | TEXT     | ICAO code of the estimated departure airport                                          | EDDM                             |
| lastSeenTime        | DATETIME | Estimated time of arrival for the flight as Unix time (seconds since epoch)           | 2018-06-24 06:55:58              |
| estArrivalAirport   | TEXT     | ICAO code of the estimated arrival airport                                            | LIDU                             |
| callsign            | TEXT     | Callsign of the aircraft                                                              | DLA3SM                           |


## Imagined scenarios

- What to do if the data was increased by 100x:  
  If the data were to be increased by 100 times, one should think about a distributed database in a cloud such as AWS Redshift, since Redshift is highly scalable and is designed for large amounts of data. High query speeds are also possible there thanks to the physical distribution of resources over a cluster structure and the parallelization of processing.
- What to do if the pipelines were run on a daily basis by 7am:  
  Then the parameter 'schedule_interval' should be adjusted accordingly in the DAG configuration.
- What to do if the database needed to be accessed by 100+ people:  
  Then you should think about a front end to increase user-friendliness. For this purpose, a user and role concept should also be implemented.

## Conclusion
I found the project very interesting and I had a lot of fun. Since I find the aircraft world very exciting, I decided to create a data set about historical flights by querying various sources. At the beginning of the project, I started looking for suitable sources with the focus on open source and open data, as I mentioned at the beginning of this README. Fortunately, I found what I was looking for, even if not all the data available are complete. Then I set about implementing an ETL pipeline with Apache Airflow to extract the data, transfer it and load it into the database, in this case PostgreSQL. Data quality checks were also carried out. Thus the necessary data is now in dimension tables and fact tables to be able to execute queries. I wish everyone who wants to use this repository as the basis for their own project a lot of fun!