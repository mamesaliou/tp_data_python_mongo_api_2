from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load import load_data

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 1),
    'retries': 1,
}

dag = DAG(
    'spotify_pipeline',
    default_args=default_args,
    description='Spotify Pipeline DAG',
    schedule_interval='@daily',
)

def run_extract():
    data = extract_data('data/SpotifyHistory.csv')
    return data

def run_transform(data):
    transformed_data = transform_data(data)
    return transformed_data

def run_load(data):
    load_data(data, 'spotify_history', 'listening_history')

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=run_extract,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=lambda **kwargs: run_transform(kwargs['ti'].xcom_pull(task_ids='extract_data')),
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=lambda **kwargs: run_load(kwargs['ti'].xcom_pull(task_ids='transform_data')),
    dag=dag,
)

extract_task >> transform_task >> load_task
