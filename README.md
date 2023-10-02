# Strava Data Integration

## Overview
This project demonstrates the process of integrating Strava API data into a Snowflake data warehouse using dbt (Data Build Tool) and Airflow. 

By following this project, you can learn how to collect and analyze your Strava fitness data in a structured and automated way.

<img width="1788" alt="image" src="https://github.com/GabsGear/strava-data-integration/assets/20424895/e3ceae11-3c69-46c7-bbb6-3e0d18a44c66">


[Here a example dashboard with this data](https://lookerstudio.google.com/reporting/a8e8d37e-5730-4db0-ae0d-04e9a0a4cb6d)


## Prerequisites
For run this project you will need [Docker Compose](https://docs.docker.com/compose/)

#### Strava API Integration
Sign up for a Strava Developer Account (https://developers.strava.com/).

Create a new OAuth Application on the Strava Developer Dashboard and obtain your client_id and client_secret.

### SnowFlake Warehouse
You will needs a snowflake project, with the following structure

```
SNOWFLAKE_SCHEMA = 'STRAVA'
SNOWFLAKE_WAREHOUSE = 'transforming'    
SNOWFLAKE_DATABASE = 'analytics'
```


[In airflow create a connection called snowflake_default](http://localhost:8080/connection/list/)


## Setup

Clone this repository to your local machine:

```
   git clone https://github.com/yourusername/strava-data-integration.git
```

Setup your strava keys, snowflake account and airflow local authentication on the .env file, like this:

```
#Airflow configuration setup

AIRFLOW_UID=1000
AIRFLOW_USER=admin
AIRFLOW_PASS=admin

#strava
STRAVA_CLIENT_ID=
STRAVA_CLIENT_SECRET=
STRAVA_REFRESH_TOKEN=

#Snowflake
SNOWFLAKE_ACCOUNT=


#Tags of images
REDIS_TAG=7.0.0
POSTGRES_TAG=13
MINIO_TAG=RELEASE.2021-10-23T03-28-24Z
MC_TAG=RELEASE.2021-11-05T10-05-06Z

```


## Usage
Create the docker image running

```
 docker compose up
```

A docker instance will run on

```
localhost:8080
```

You will see two dags, when you run create_raw_tables, airflow will get data from your strava account, transform it and send to Snowflake.

<img width="2240" alt="image" src="https://github.com/GabsGear/strava-data-integration/assets/20424895/d9c2f4ec-64c3-4ca1-acd0-e8fdea73c0c6">


The final snowflake table will be in:

```
analytics.strava."ACTIVITIES"
```


## Contributing
Contributions are welcome! If you'd like to enhance this project, feel free to fork it and submit a pull request.



