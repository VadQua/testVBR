import os
from datetime import datetime, timedelta
import requests
import csv
from clickhouse_driver import Client
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 8),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

### КОД ДЛЯ СОЗДАНИЯ ТАБЛИЦЫ
# CREATE TABLE IF NOT EXISTS page_metrics (
#     url String,
#     lcp Float64,
#     tbt Float64,
#     date Date,
#     PRIMARY KEY (url, date)
# ) ENGINE = MergeTree()
# ORDER BY (url, date);

dag = DAG(
    'collect_page_metrics_daily',
    default_args=default_args,
    description='A DAG to collect Google PageSpeed Insights metrics daily and save to ClickHouse',
    schedule_interval=timedelta(days=1),
)

def load_urls_from_csv():
    url = "https://github.com/grimlyrosen/tests/raw/e04d9b18d0d2e087045e01b75d18aa0c21ce504a/urllist.csv"
    response = requests.get(url)
    with open("/tmp/urllist.csv", "wb") as f:
        f.write(response.content)

def collect_and_save_metrics():
    api_key = os.getenv("API_KEY")

    with open("/tmp/urllist.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            url = row[0]
            api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={api_key}"
            response = requests.get(api_url)
            data = response.json()
            lcp = data['loadingExperience']['metrics']['LARGEST_CONTENTFUL_PAINT_MS']['percentile']
            tbt = data['loadingExperience']['metrics']['EXPERIMENTAL_TIME_TO_FIRST_BYTE']['percentile']

            with open("/tmp/page_metrics.csv", mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([url, lcp, tbt, datetime.now().strftime('%Y-%m-%d')])

            client = Client(host='clickhouse_host', port=8123, user='default', password='default', database='default')
            query = f"""INSERT INTO page_metrics (url, lcp, tbt, date)
                        VALUES ('{url}', {lcp}, {tbt}, now())
                        ON DUPLICATE KEY UPDATE lcp = {lcp}, tbt = {tbt}, date = now()"""
            client.execute(query)

load_urls_task = PythonOperator(
    task_id='load_urls_from_csv',
    python_callable=load_urls_from_csv,
    dag=dag,
)

collect_metrics_task = PythonOperator(
    task_id='collect_and_save_metrics',
    python_callable=collect_and_save_metrics,
    dag=dag,
)

load_urls_task >> collect_metrics_task
