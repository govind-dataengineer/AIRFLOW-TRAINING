"""
ADVANCED: Dynamic Task Generation
Tags: ['advanced', 'dynamic-tasks', 'loop']

This DAG demonstrates:
- Dynamically generating tasks based on a list
- Mapping operator (parallel task generation)
- Processing multiple items in a scalable way

Key Concepts:
- Creating multiple tasks from a loop
- Task naming conventions for dynamic tasks
- Processing collections of items in parallel
- Using task_id templates
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'start_date': datetime(2024, 1, 1),
}

# List of items to process
ITEMS_TO_PROCESS = ['item_a', 'item_b', 'item_c', 'item_d', 'item_e']

def process_item(item):
    """Process a single item"""
    print(f"Processing: {item}")
    # Simulate processing
    result = {
        'item': item,
        'processed_at': datetime.now().isoformat(),
        'status': 'completed'
    }
    print(f"Result: {result}")
    return result

def aggregate_results(**context):
    """Aggregate results from all dynamic tasks"""
    print("Aggregating results from all items...")
    print(f"Number of items processed: {len(ITEMS_TO_PROCESS)}")
    print(f"Items: {ITEMS_TO_PROCESS}")

# Create the DAG
with DAG(
    dag_id='08_advanced_dynamic_tasks',
    default_args=default_args,
    description='DAG with dynamically generated tasks',
    schedule_interval='@daily',
    catchup=False,
    tags=['advanced', 'dynamic-tasks'],
) as dag:
    
    start = PythonOperator(
        task_id='start',
        python_callable=lambda: print("Processing items dynamically"),
    )
    
    # Dynamically create tasks for each item
    dynamic_tasks = []
    for item in ITEMS_TO_PROCESS:
        task = PythonOperator(
            task_id=f'process_{item}',
            python_callable=process_item,
            op_kwargs={'item': item},  # Pass item to the function
            doc_md=f"Process {item}"
        )
        dynamic_tasks.append(task)
    
    aggregate = PythonOperator(
        task_id='aggregate_results',
        python_callable=aggregate_results,
        provide_context=True,
        doc_md="Aggregate results from all dynamic tasks"
    )
    
    # Dependencies: start -> [all dynamic tasks] -> aggregate
    start >> dynamic_tasks >> aggregate
