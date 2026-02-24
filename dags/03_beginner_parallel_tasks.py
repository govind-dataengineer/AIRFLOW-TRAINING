"""
BEGINNER: Parallel Tasks
Tags: ['beginner', 'parallel-tasks']

This DAG demonstrates:
- Multiple tasks running in parallel (simultaneously)
- Different task dependency patterns
- How Airflow schedules parallel execution

Key Concepts:
- Tasks with no inter-dependencies can run in parallel
- Mixed sequential and parallel patterns
- Improving DAG execution time with parallelization
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 0,
    'start_date': datetime(2024, 1, 1),
}

# Task functions
def start_task():
    print("Starting pipeline...")
    return "Pipeline started"

def process_data_1():
    print("Processing data batch 1...")
    import time
    time.sleep(2)  # Simulate work
    print("Batch 1 completed")

def process_data_2():
    print("Processing data batch 2...")
    import time
    time.sleep(2)  # Simulate work
    print("Batch 2 completed")

def process_data_3():
    print("Processing data batch 3...")
    import time
    time.sleep(2)  # Simulate work
    print("Batch 3 completed")

def consolidate_results():
    print("Consolidating results...")
    print("All batches processed and consolidated")

# Create the DAG
with DAG(
    dag_id='03_beginner_parallel_tasks',
    default_args=default_args,
    description='DAG with parallel task execution',
    schedule_interval='@daily',
    catchup=False,
    tags=['beginner', 'parallel'],
) as dag:
    
    start = PythonOperator(
        task_id='start',
        python_callable=start_task,
    )
    
    # These three tasks will run in parallel
    process_1 = PythonOperator(
        task_id='process_batch_1',
        python_callable=process_data_1,
    )
    
    process_2 = PythonOperator(
        task_id='process_batch_2',
        python_callable=process_data_2,
    )
    
    process_3 = PythonOperator(
        task_id='process_batch_3',
        python_callable=process_data_3,
    )
    
    consolidate = PythonOperator(
        task_id='consolidate',
        python_callable=consolidate_results,
    )
    
    # Dependencies: start -> [batch1, batch2, batch3] -> consolidate
    start >> [process_1, process_2, process_3] >> consolidate
