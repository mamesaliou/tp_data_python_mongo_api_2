pip install -r requirements.txt

airflow scheduler
airflow webserver

uvicorn fastapi_app.main:app --reload
