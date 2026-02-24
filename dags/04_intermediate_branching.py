"""
INTERMEDIATE: Branching Logic (if-else conditions)
Tags: ['intermediate', 'branching', 'conditional']

This DAG demonstrates:
- Using BranchPythonOperator to create conditional logic
- Different execution paths based on conditions
- Dynamic workflow routing

Key Concepts:
- BranchPythonOperator for conditional execution
- Task IDs that dynamically determine which task runs next
- Handling multiple workflow paths
"""

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime, timedelta
import random

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

def check_value():
    """
    Decision point: Generate a random number and decide which path to take
    Returns the task_id of the next task to execute
    """
    value = random.randint(1, 100)
    print(f"Generated value: {value}")
    
    if value < 33:
        print("Route: Low value path")
        return 'low_value_task'
    elif value < 66:
        print("Route: Medium value path")
        return 'medium_value_task'
    else:
        print("Route: High value path")
        return 'high_value_task'

def low_value_task():
    print("Processing LOW value... (< 33)")
    print("Applying discount of 50%")

def medium_value_task():
    print("Processing MEDIUM value... (33-66)")
    print("Applying discount of 25%")

def high_value_task():
    print("Processing HIGH value... (> 66)")
    print("Applying discount of 10%")

def final_task():
    print("All paths complete. Writing results.")

# Create the DAG
with DAG(
    dag_id='04_intermediate_branching',
    default_args=default_args,
    description='DAG with branching logic/conditional execution',
    schedule_interval='@daily',
    catchup=False,
    tags=['intermediate', 'branching', 'conditional'],
) as dag:
    
    start = PythonOperator(
        task_id='start',
        python_callable=lambda: print("Pipeline started"),
    )
    
    # Branch task - decides which path to take
    branching = BranchPythonOperator(
        task_id='check_value',
        python_callable=check_value,
        doc_md="Evaluates a value and determines execution path"
    )
    
    # Three possible paths
    low = PythonOperator(
        task_id='low_value_task',
        python_callable=low_value_task,
    )
    
    medium = PythonOperator(
        task_id='medium_value_task',
        python_callable=medium_value_task,
    )
    
    high = PythonOperator(
        task_id='high_value_task',
        python_callable=high_value_task,
    )
    
    # Final task that runs after any of the branches complete
    end = PythonOperator(
        task_id='final_task',
        python_callable=final_task,
        trigger_rule='one_success',  # Execute even if one of the branches succeeds
    )
    
    # Dependencies: start -> branching -> [low/medium/high] -> end
    start >> branching >> [low, medium, high] >> end
