from datetime import datetime

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from get_data_from_postgresql import read_from_db, get_tables_list


tables_list = get_tables_list()
print(tables_list)

default_args = {
    'owner': 'airflow',
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'retries': 2
}

dag = DAG(
    'get_data_from_postgresql',
    description='get_data_from_postgresql_and_put_to_folder',
    schedule_interval='@daily',
    start_date=datetime(2021,11,11),
    end_date=datetime(2021,12,11),
    default_args=default_args
)


for i in get_tables_list():
    task = PythonOperator(
        task_id='load_' + i,
        python_callable = read_from_db,
        op_kwargs={'st': i},
        dag=dag
    )
