from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from get_data_from_API import app



default_args = {
    'owner': 'airflow',
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'retries': 2
}

dag = DAG(
    'get_data_from_API',
    description='get_data_from_API_and_put_to_folder',
    schedule_interval='@daily',
    start_date=datetime(2021,10,20),
    end_date=datetime(2021,11,20),
    default_args=default_args
)

t1 = PythonOperator(
    task_id='get_data',
    dag=dag,
    python_callable=app
)

import pandas
from zipfile import ZipFile
from boto3.session import Session
session=Session()
s3 = session.resource('s3')
b = s3.Bucket()