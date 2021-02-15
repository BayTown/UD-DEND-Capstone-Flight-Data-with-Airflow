# Udacity Data Engineering Nanodegree - Project 6/6
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=flat-square&logo=python)](https://www.python.org/)
[![made-with-apache-airflow](https://img.shields.io/badge/Made%20with-Apache%20Airflow-blue.svg?logo=apache-airflow)](https://airflow.apache.org/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square&logo=appveyor)](https://lbesson.mit-license.org/)

## Capstone Project - Flight Data with Airflow


## Introduction  

    What's the goal? What queries will you want to run?

This project is about historical flight data. It is about extracting historical flight data (facts)
and additional information (dimensions) from various sources, transforming them and loading them into a structured
data warehouse in order to make this data available for data analysis.  
If the project is successfully implemented, you should be able to search through the data warehouse, e.g. when at which airport which aircraft took off. Or how many aircraft have flown to a specific airport on a specific day.


## Project Description
    
    How would Spark or Airflow be incorporated? Why did you choose the model you chose?
    Clearly state the rationale for the choice of tools and technologies for the project.
    The choice of tools, technologies are justified well.

In this project I extracted the required data from two different data sources (OpenSky Network and Python traffic API), then put them into a meaningful context using transform and then finally loaded the data into a database in the form of fact and dimension tables.  
When it comes to data sources, the OpenSource and OpenData concept was very important to me, as I believe that this will be the driver for our future world. Even if, as I will explain below, I had to accept a few flaws.  

I chose Apache Airflow and PostgreSQL as the technological basis to realize this project.

- [Apache Airflow](https://airflow.apache.org/)  
Apache Airflow is an open-source workflow management platform. Airflow allows to programmatically author and schedule their workflows and monitor them via the built-in Airflow user interface. Airflow is written in Python, and workflows are created via Python scripts. Airflow is designed under the principle of "configuration as code".

- [PostgreSQL](https://www.postgresql.org/)  
PostgreSQL also known as Postgres, is a free and open-source relational database management system (RDBMS) emphasizing extensibility and SQL compliance.

In this project I will use Apache Airflow to cyclically extract the data from the required data sources. And Postgres to load this transformed data into the database. This then functions as a data warehouse.

## Requirements

This project was done on a Linux-OS ([Ubuntu 20.04 LTS](https://ubuntu.com/download/desktop)) with the source-code editor [Visual Studio Code](https://code.visualstudio.com/).

To implement the project you will need the following things:

- [Python](https://www.python.org/) Version 3.8.5
- [Apache Airflow](https://airflow.apache.org/) Version 2.0.0
- [PostgreSQL](https://www.postgresql.org/) Version 12.5

## Project Datasets - Data Sources
    The project includes:

    At least 2 data sources
    More than 1 million lines of data.
    At least two data sources/formats (csv, api, json)

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
Document the steps of the process.
Propose how often the data should be updated and why.

### Data Quality Checks
staging_aircraft_database.icao24

## Database schema
The purpose of the final data model is made explicit.
A data dictionary for the final data model is included.


## Conclusion


    
## Scenarios
    Include a description of how you would approach the problem differently under the following scenarios:
        If the data was increased by 100x.
        If the pipelines were run on a daily basis by 7am.
        If the database needed to be accessed by 100+ people.
