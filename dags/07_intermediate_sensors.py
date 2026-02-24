"""
INTERMEDIATE: Sensors and Waiting for External Events
Tags: ['intermediate', 'sensors', 'file-operations']

This DAG demonstrates:
- Sensors that wait for conditions/files
- File operations
- Polling for external events

Key Concepts:
- FileSensor to wait for file creation
- PythonOperator creating files
- Conditional task execution based on external events
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
import os
import time

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

def create_marker_file():
    """Create a marker file that the sensor will wait for"""
    output_dir = '/tmp/airflow_demo'
    os.makedirs(output_dir, exist_ok=True)
    
    marker_file = os.path.join(output_dir, 'data_ready.txt')
    print(f"Creating marker file: {marker_file}")
    
    # Simulate some delay
    time.sleep(2)
    
    with open(marker_file, 'w') as f:
        f.write("Data is ready for processing\n")
        f.write(f"Created at: {datetime.now()}\n")
    
    print(f"Marker file created successfully")

def process_after_file():
    """Process the data after the file is detected by sensor"""
    marker_file = '/tmp/airflow_demo/data_ready.txt'
    
    if os.path.exists(marker_file):
        with open(marker_file, 'r') as f:
            print("Contents of marker file:")
            print(f.read())
    else:
        print("Marker file not found!")

# Create the DAG
with DAG(
    dag_id='07_intermediate_sensors',
    default_args=default_args,
    description='DAG with Sensors - waiting for external events',
    schedule_interval='@daily',
    catchup=False,
    tags=['intermediate', 'sensors'],
) as dag:
    
    start = PythonOperator(
        task_id='start_task',
        python_callable=lambda: print("Pipeline started"),
    )
    
    create_file = PythonOperator(
        task_id='create_marker_file',
        python_callable=create_marker_file,
        doc_md="Creates a marker file for the sensor to detect"
    )
    
    # Sensor that waits for the file (timeout after 60 seconds)
    wait_for_file = FileSensor(
        task_id='wait_for_data_file',
        filepath='/tmp/airflow_demo/data_ready.txt',
        fs_conn_id='fs_default',
        poke_interval=2,  # Check every 2 seconds
        timeout=60,  # Timeout after 60 seconds
        doc_md="Waits for data_ready.txt file to appear"
    )
    
    process = PythonOperator(
        task_id='process_file',
        python_callable=process_after_file,
        doc_md="Processes the data after file is detected"
    )
    
    # Dependencies
    start >> create_file >> wait_for_file >> process
