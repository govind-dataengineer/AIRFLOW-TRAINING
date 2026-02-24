"""
INTERMEDIATE: Error Handling and Retries
Tags: ['intermediate', 'error-handling', 'retries']

This DAG demonstrates:
- Retry mechanisms with exponential backoff
- Error handling with try-except
- Handling failures gracefully
- Task SLA (Service Level Agreement)

Key Concepts:
- Configuring retry attempts and delays
- Custom error handling in tasks
- SLA monitoring
- Alerting on task failures
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import random

default_args = {
    'owner': 'airflow',
    'retries': 3,  # Retry up to 3 times
    'retry_delay': timedelta(minutes=1),  # Wait 1 minute before retrying
    'start_date': datetime(2024, 1, 1),
}

attempt_count = {'count': 0}

def unstable_task():
    """
    This task simulates an unstable operation that might fail
    It will fail the first 2 attempts, then succeed
    """
    attempt_count['count'] += 1
    print(f"Attempt #{attempt_count['count']}")
    
    if attempt_count['count'] < 3:
        raise Exception(f"Task failed on attempt {attempt_count['count']}. Retrying...")
    else:
        print(f"Success on attempt {attempt_count['count']}!")

def task_with_error_handling():
    """
    Task with built-in error handling
    """
    try:
        print("Attempting risky operation...")
        # Simulate a risky operation
        value = 10 / 0  # This will raise an exception
    except ZeroDivisionError as e:
        print(f"Caught error: {e}")
        print("Handling error gracefully... using default value")
        value = 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise  # Re-raise if we want Airflow to mark this as failed
    
    print(f"Operation completed with value: {value}")

def reliable_task():
    """
    A task that always succeeds
    """
    print("This task always completes successfully")

def cleanup_task(ti):
    """
    Cleanup task that runs regardless of success/failure
    """
    print("Running cleanup operations...")
    
    # Check previous task status
    previous_state = ti.state
    print(f"Previous task state: {previous_state}")

# Create the DAG
with DAG(
    dag_id='05_intermediate_error_handling',
    default_args=default_args,
    description='DAG demonstrating error handling and retries',
    schedule_interval='@daily',
    catchup=False,
    tags=['intermediate', 'error-handling', 'retries'],
    sla=timedelta(hours=1),  # SLA: Must complete within 1 hour
) as dag:
    
    task1 = PythonOperator(
        task_id='unstable_task',
        python_callable=unstable_task,
        retries=3,  # Override default retries for this task
        retry_delay=timedelta(seconds=30),  # Retry after 30 seconds
        doc_md="This task demonstrates retry mechanism"
    )
    
    task2 = PythonOperator(
        task_id='task_with_error_handling',
        python_callable=task_with_error_handling,
        retries=1,  # Only retry once for this task
        doc_md="Task with built-in error handling"
    )
    
    task3 = PythonOperator(
        task_id='reliable_task',
        python_callable=reliable_task,
        retries=0,  # No retries needed for this reliable task
        doc_md="A reliable task"
    )
    
    cleanup = PythonOperator(
        task_id='cleanup_task',
        python_callable=cleanup_task,
        trigger_rule='all_done',  # Run regardless of success/failure
        doc_md="Cleanup that runs whether tasks succeed or fail"
    )
    
    # Dependencies
    [task1, task2, task3] >> cleanup
