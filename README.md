python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

[core]
# The folder where your airflow pipelines live, most likely a
# subfolder in a code repository. This path must be absolute.
#
# Variable: AIRFLOW__CORE__DAGS_FOLDER
#
#dags_folder = /home/codespace/airflow/dags
dags_folder = /workspaces/tp_data_python_mongo_api_2/dags/

[webserver]
enable_proxy_fix = True

airflow standalone

uvicorn fastapi_app.main:app --reload
