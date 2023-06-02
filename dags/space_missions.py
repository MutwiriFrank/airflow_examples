# 1 download json 
# 2 get first 20 images
# 3 notify

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
import requests
import json
from datetime import datetime, timedelta
import pathlib

default_args ={
    "email" : ["franklinmutwiri41@gmail.com"],
    "email_on_failure" :False,
    "email_on_retry" : False,
    "retries" : 5,
    "retry_delay" : timedelta(minutes=3),
    "depends_on_past" : True,
    "wait_for_downstream" : True
}

def download_images():
    with open("launches.json", "w") as f:
        response = requests.get('https://ll.thespacedevs.com/2.0.0/launch/upcoming')
        json.dump(response.json(), f)
        f.close()

def get_images():
    with open("launches.json") as f:
    # Ensure directory exists
        pathlib.Path("/airflow/images").mkdir(parents=True, exist_ok=True)

        launches = json.load(f)
        image_urls = [launch["image"] for launch in launches["results"] ]
        for url in image_urls:
        # try:
            response = requests.get(url)
            image_name = url.split("/")[-1]
            target_file =  f"../images/{image_name}"
            with open (target_file, "wb" ) as target:
                # print(target_file)
                target.write(response.content)
            print(f"Downloaded {url} to {target_file}")
        

with DAG ( 
    dag_id = "space_missions",
    start_date= datetime(2023,5,28,12),
    default_args=default_args,
    schedule= "@daily",
    max_active_runs=3
) as dag:

    download_images = PythonOperator(
        task_id ="download_images",
        python_callable=download_images
    )

    get_images = PythonOperator(
        task_id = "get_images",
        python_callable=get_images
    )

    send_email_notification = EmailOperator(
        task_id = "send_email_notification",
        to = "mutwiriben813@gmail.com",
        subject="get space launches",
        html_content="<h3>Rocket launches done</h3>"
    )

    download_images >> get_images >> send_email_notification
