import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG(
dag_id="templating",
start_date=airflow.utils.dates.days_ago(3),
schedule="@hourly",
)

'''
DOuble curly bracrs denote a variable inserted at runtime
any python variable or expression can be provided
'''

get_data = BashOperator(
task_id="get_data",
bash_command=(
"curl -o /tmp/wikipageviews.gz "
"https://dumps.wikimedia.org/other/pageviews/"
"{{ execution_date.year }}/"
"{{ execution_date.year }}-"
"{{ '{:02}'.format(execution_date.month) }}/"
"pageviews-{{ execution_date.year }}"
"{{ '{:02}'.format(execution_date.month) }}"
"{{ '{:02}'.format(execution_date.day) }}-"
"{{ '{:02}'.format(execution_date.hour) }}0000.gz"
),
dag=dag,
)