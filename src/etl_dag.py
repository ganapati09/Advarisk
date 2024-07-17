from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import extract_clean_data as etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='ETL pipeline that runs every 3 hours',
    schedule_interval=timedelta(hours=3),
)

def run_etl():
    data = etl.extract_data()
    data = etl.clean_data(data)
    agg_df = etl.transform_data(data)
    insights = etl.generate_insights(agg_df)
    etl.load_data(agg_df, insights)

run_etl_task = PythonOperator(
    task_id='run_etl',
    python_callable=run_etl,
    dag=dag,
)

run_etl_task
