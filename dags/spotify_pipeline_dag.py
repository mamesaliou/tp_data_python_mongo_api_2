from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

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

extract_task = BashOperator(
    task_id='extract_data',
    bash_command='python /workspaces/tp_data_python_mongo_api_2/scripts/extract.py',
    dag=dag,
)

transform_task = BashOperator(
    task_id='transform_data',
    bash_command='python /workspaces/tp_data_python_mongo_api_2/scripts/transform.py',
    dag=dag,
)

load_task = BashOperator(
    task_id='load_data',
    bash_command='python /workspaces/tp_data_python_mongo_api_2/scripts/load.py',
    dag=dag,
)

extract_task >> transform_task >> load_task
