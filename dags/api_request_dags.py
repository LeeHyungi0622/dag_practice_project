from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator

from datetime import datetime

with DAG(
    "api_request_dag",
    start_date=datetime(2022, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='fast_api',
        endpoint='/search?q="python'
    )

    send_request = SimpleHttpOperator(
        task_id='send_request',
        method='GET',
        http_conn_id='fast_api',
        endpoint='/search?q="python',
        response_filter=lambda response: response.text,
        log_response=True
    )

    is_api_available >> send_request