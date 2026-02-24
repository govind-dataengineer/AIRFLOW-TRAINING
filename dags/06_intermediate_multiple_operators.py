"""
INTERMEDIATE: Multiple Operators
Tags: ['intermediate', 'multiple-operators', 'bash']

This DAG demonstrates:
- Using different types of operators (Python, Bash, Email)
- Operator composition
- Mixing different task types

Key Concepts:
- PythonOperator for Python code execution
- BashOperator for shell commands
- EmailOperator for notifications
- Combining different operators in one DAG
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

def python_function():
    """Python task"""
    print("Executing Python function")
    with open('/tmp/python_output.txt', 'w') as f:
        f.write("This is output from Python task\n")
    return "Python task completed"

def another_python_task():
    """Another Python task that reads the previous output"""
    try:
        with open('/tmp/python_output.txt', 'r') as f:
            content = f.read()
        print(f"Read from file: {content}")
    except FileNotFoundError:
        print("File not found")

# Create the DAG
with DAG(
    dag_id='06_intermediate_multiple_operators',
    default_args=default_args,
    description='DAG with different operator types',
    schedule_interval='@daily',
    catchup=False,
    tags=['intermediate', 'multiple-operators'],
) as dag:
    
    python_task1 = PythonOperator(
        task_id='python_task_1',
        python_callable=python_function,
        doc_md="First Python task"
    )
    
    bash_task = BashOperator(
        task_id='bash_task',
        bash_command='echo "Hello from Bash" && date && cat /tmp/python_output.txt',
        doc_md="Bash task that echoes messages and shows the date"
    )
    
    python_task2 = PythonOperator(
        task_id='python_task_2',
        python_callable=another_python_task,
        doc_md="Second Python task that reads from file"
    )
    
    bash_cleanup = BashOperator(
        task_id='bash_cleanup',
        bash_command='rm -f /tmp/python_output.txt && echo "Cleanup completed"',
        doc_md="Cleanup bash task"
    )
    
    # Dependencies: python1 -> bash -> python2 -> bash_cleanup
    python_task1 >> bash_task >> python_task2 >> bash_cleanup
