from urllib import request
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
import logging

logger = logging.getLogger(__name__)

dag = DAG(
    dag_id="stocksense",
    start_date=airflow.utils.dates.days_ago(2),
    schedule_interval="@hourly"
)

def _get_data(logical_date):
    # logger.info(f"The execution date of this flow is {ds.month}")
    year = logical_date.year
    month = logical_date.month
    day = logical_date.day
    hour = logical_date.hour
    url = ( 
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:0>2}/"
        f"pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )
    output_path = "./wikipageviews.gz"
    request.urlretrieve(url, output_path)
get_data = PythonOperator(
    task_id="get_data",
    python_callable=_get_data,
    dag= dag
)