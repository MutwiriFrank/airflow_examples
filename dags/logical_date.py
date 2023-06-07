from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta 
import logging

logger = logging.getLogger(__name__)

dag = DAG(
  dag_id="sample_dag",
  schedule="@daily",
  start_date=datetime(2023, 5, 21),
)

def _print_execution_date(ds):
  print(f"The execution date of this flow is {ds}")
  logger.info(f"The execution date of this flow is {ds}")

print_dag = PythonOperator(
  task_id='print_task',
  python_callable=_print_execution_date,
  dag=dag,
)