# Strava Data Integration

## Overview
This project demonstrates the process of integrating Strava API data into a Snowflake data warehouse using dbt (Data Build Tool) and Airflow. By following this project, you can learn how to collect and analyze your Strava fitness data in a structured and automated way.

## Prerequisites
Before you begin, ensure you have the following prerequisites:
- Python 3.x
- Docker 
- Strava Developer Account (to access the Strava API)
- Snowflake Account (with necessary credentials)
- dbt  
- Apache Airflow  

## Project Structure

``` 
strava-data-integration/
│
├── strava/
│ ├── strava_api.py
│ └── config.yaml
│
├── snowflake/
│ ├── snowflake-dbt-models/
│ │ └── ...
│ └── dbt_profiles.yml
│
├── airflow/
│ ├── dags/
│ │ └── strava_data_dag.py
│ └── plugins/
│ └── ...
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Setup
1. Clone this repository to your local machine:
```
   git clone https://github.com/yourusername/strava-data-integration.git
```

Set up your Strava API credentials by creating a config.yaml file in the strava/ directory with your client_id and client_secret:

```
strava:
  client_id: YOUR_CLIENT_ID
  client_secret: YOUR_CLIENT_SECRET
```

## Strava API Integration
Sign up for a Strava Developer Account (https://developers.strava.com/).

Create a new OAuth Application on the Strava Developer Dashboard and obtain your client_id and client_secret.

Update the config.yaml file with the client_id and client_secret you obtained from Strava.

## Data Warehouse Setup
Set up Snowflake and create a database and schema for this project.

Configure your Snowflake connection details in the snowflake/dbt_profiles.yml file.

Create the necessary tables and schemas in Snowflake according to your dbt models.

## ETL Process with dbt
Define your data models using dbt in the snowflake-dbt-models directory.

Run dbt to build and test your models:

bash
Copy code
dbt run
Deploy your dbt models to Snowflake:

```
dbt seed
dbt run
dbt test
```

## Automating with Airflow
Configure your Airflow connection settings in the Airflow UI or in airflow/dags/strava_data_dag.py.

Create and activate a virtual environment for your Airflow project.

Start the Airflow scheduler and web server:

```
airflow scheduler
airflow webserver --port 8080
Access the Airflow web UI at http://localhost:8080 and trigger the strava_data_dag DAG.
```

## Usage
Once the project is set up and the DAG is running in Airflow, your Strava data will be automatically fetched, transformed, and loaded into your Snowflake data warehouse on a regular basis.
You can create your own visualizations or analyses using tools like Looker, Tableau, or any BI tool of your choice.

## Contributing
Contributions are welcome! If you'd like to enhance this project, feel free to fork it and submit a pull request.



