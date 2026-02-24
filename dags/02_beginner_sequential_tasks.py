"""
BEGINNER: Sequential Tasks with Dependencies
Tags: ['beginner', 'dependencies']

This DAG demonstrates:
- Multiple tasks in sequence
- Task dependencies (one task must complete before the next starts)
- Passing data between tasks using XCom (cross-communication)

Key Concepts:
- Defining multiple PythonOperators
- Using the >> operator to define task dependencies
- Basic XCom communication between tasks
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

# Task 1: Extract
def extract_data():
    print("Extracting data...")
    data = {
        'users': ['Alice', 'Bob', 'Charlie'],
        'scores': [85, 90, 78]
    }
    print(f"Extracted: {data}")
    return data  # This will be pushed to XCom

# Task 2: Transform
def transform_data(ti):
    # ti is the task instance - used to pull data from XCom
    data = ti.xcom_pull(task_ids='extract_task')
    print(f"Received data: {data}")
    
    # Transform: Add 10 points to each score
    transformed = {
        'users': data['users'],
        'scores': [score + 10 for score in data['scores']]
    }
    print(f"Transformed: {transformed}")
    return transformed

# Task 3: Load
def load_data(ti):
    data = ti.xcom_pull(task_ids='transform_task')
    print(f"Loading data: {data}")
    print("Data loaded successfully!")

# Create the DAG
with DAG(
    dag_id='02_beginner_sequential_tasks',
    default_args=default_args,
    description='DAG with sequential tasks and dependencies',
    schedule_interval='@daily',
    catchup=False,
    tags=['beginner', 'dependencies', 'etl'],
) as dag:
    
    # Create tasks
    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_data,
        doc_md="Extract data from source"
    )
    
    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_data,
        doc_md="Transform extracted data"
    )
    
    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load_data,
        doc_md="Load transformed data"
    )
    
    # Define dependencies: extract -> transform -> load
    extract_task >> transform_task >> load_task
