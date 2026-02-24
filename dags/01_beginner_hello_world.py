"""
BEGINNER: Hello World DAG
Tags: ['beginner', 'hello-world']

This is the simplest possible DAG. It contains a single task that prints "Hello, Airflow!"
Perfect for verifying your Airflow installation and understanding basic DAG structure.

Key Concepts:
- DAG creation with basic parameters
- Single PythonOperator task
- How to run your first DAG
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

# Define a simple Python function
def hello_world():
    print("Hello, Airflow! This is your first DAG!")
    return "Task completed successfully"

# Create the DAG
with DAG(
    dag_id='01_beginner_hello_world',
    default_args=default_args,
    description='The simplest possible Airflow DAG',
    schedule_interval='@daily',  # Run once per day
    catchup=False,  # Don't run past DAG runs
    tags=['beginner', 'hello-world'],
) as dag:
    
    # Create a simple task
    hello_task = PythonOperator(
        task_id='hello_task',
        python_callable=hello_world,
        doc_md="""
        ### Hello World Task
        This task simply prints a hello message.
        """
    )

# Note: With only one task, there are no dependencies to define
