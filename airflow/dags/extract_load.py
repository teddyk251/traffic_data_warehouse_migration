from asyncore import read
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python_operator import PythonOperator
from datetime import datetime as dt
from datetime import timedelta
from airflow import DAG 
import pandas as pd
from sqlalchemy import Numeric
import sys
import os
sys.path.append(os.path.abspath("../scripts/"))
from datareader import DataReader
import db_connector

# Specifing the default_args
default_args = {
    'owner': 'tewodros',
    'depends_on_past': False,
    'email': ['teddylnk1@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'start_date': dt(2022, 7, 22),
    'retry_delay': timedelta(minutes=5)
}

dr = DataReader()
 
# Extract data to be loaded
def read_data(ti):
    vehicle, trajectories = dr.extract_data('/opt/airflow/data/20181024_d1_0830_0900.csv')

    data = {'vehicle':vehicle, 'trajectories':trajectories}
    ti.xcom_push(key='raw_dataframes', value=data)

# Create the tables
def create_table():
    db_connector.create_table()
  


# Inserting the data into the our postgres table
def insert_data(ti): 
    data = ti.xcom_pull(key="raw_dataframes", task_ids='read_data')
    for name in data.keys():

        db_connector.insert_table(data[name], name)

    

# Dag creation
with DAG(
    dag_id='data_to_Postgres_loader_dag',
    default_args=default_args,
    description='Upload data from CSV to Postgres',
    schedule_interval='@once',
    catchup=False
) as pg_dag:
 
    data_reader = PythonOperator(
        task_id='read_data',
        python_callable=read_data
    )

    table_creator = PythonOperator(
        task_id='table_creator',
        python_callable=create_table
    )

    insert_data = PythonOperator(
        task_id='insert_data',
        python_callable=insert_data
    )

# Task dependencies
data_reader >> table_creator >> insert_data