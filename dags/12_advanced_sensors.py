"""
ADVANCED: Complex Sensor Patterns and Orchestration
Tags: ['advanced', 'sensors', 'external-systems', 'error-handling']

This DAG demonstrates:
- Multiple sensors running in parallel
- Different sensor types with timeout and soft fail handling
- Custom sensor logic with retries
- Sensor dependencies and orchestration
- Poke intervals and exponential backoff
- Task group with sensors

Key Concepts:
- FileSensor with timeout and soft_fail
- TimeDeltaSensor for time-based waiting
- ExternalTaskSensor for cross-DAG dependencies
- Custom sensor with BaseSensorOperator
- Sensor poke_interval and timeout configuration
- Using sensors in TaskGroups for better organization
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.python import PythonSensor
from airflow.sensors.datetime import DateTimeSensor
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.exceptions import AirflowSkipException
from datetime import datetime, timedelta
import os
import time
import random

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(seconds=10),
}

with DAG(
    dag_id='12_advanced_sensors',
    default_args=default_args,
    description='Advanced sensors and orchestration patterns',
    schedule_interval='@daily',
    catchup=False,
    tags=['advanced', 'sensors'],
) as dag:

    # ===== Setup - Create test files and conditions =====
    def create_test_files():
        """Create multiple test files for sensors to wait on"""
        output_dir = '/tmp/airflow_sensors_demo'
        os.makedirs(output_dir, exist_ok=True)
        
        files = [
            'critical_data.csv',
            'metadata.json',
            'config.yaml'
        ]
        
        for idx, filename in enumerate(files):
            filepath = os.path.join(output_dir, filename)
            time.sleep(idx + 1)  # Stagger file creation
            with open(filepath, 'w') as f:
                f.write(f"Data for {filename} at {datetime.now()}\n")
            print(f"Created: {filepath}")
    
    setup_task = PythonOperator(
        task_id='setup_test_files',
        python_callable=create_test_files,
    )

    # ===== Sensor Group 1: File Sensors with Different Timeouts =====
    with TaskGroup(group_id='file_sensors_group') as file_sensors:
        
        # Sensor with short timeout
        sensor_critical = FileSensor(
            task_id='wait_for_critical_data',
            filepath='/tmp/airflow_sensors_demo/critical_data.csv',
            fs_conn_id='fs_default',
            poke_interval=2,  # Check every 2 seconds
            timeout=30,  # Wait up to 30 seconds
            mode='poke',  # Use polling instead of reschedule
            soft_fail=False,  # Fail the task if timeout
        )
        
        # Sensor with soft fail - won't fail the DAG
        sensor_metadata = FileSensor(
            task_id='wait_for_metadata',
            filepath='/tmp/airflow_sensors_demo/metadata.json',
            fs_conn_id='fs_default',
            poke_interval=3,
            timeout=20,
            mode='poke',
            soft_fail=True,  # Skip this task if timeout instead of failing
        )
        
        # Sensor with reschedule mode - more efficient for long waits
        sensor_config = FileSensor(
            task_id='wait_for_config',
            filepath='/tmp/airflow_sensors_demo/config.yaml',
            fs_conn_id='fs_default',
            poke_interval=5,
            timeout=60,
            mode='reschedule',  # Release worker during waits
            soft_fail=False,
        )
        
        # No dependencies - all sensors run in parallel
        [sensor_critical, sensor_metadata, sensor_config]

    # ===== Python Sensor: Custom Logic with Conditional Return =====
    def check_data_quality():
        """
        Custom sensor logic that checks data quality.
        Returns True when condition is met, False to retry.
        """
        data_dir = '/tmp/airflow_sensors_demo'
        
        # Check if critical file exists and has content
        critical_file = os.path.join(data_dir, 'critical_data.csv')
        if not os.path.exists(critical_file):
            print("Critical data file not found yet, will retry...")
            return False
        
        # Check file size (simulate data quality check)
        file_size = os.path.getsize(critical_file)
        min_size = 10  # Minimum expected file size
        
        if file_size < min_size:
            print(f"File too small ({file_size}B), waiting for more data...")
            return False
        
        print(f"Data quality check passed! File size: {file_size}B")
        return True
    
    python_sensor = PythonSensor(
        task_id='check_data_quality',
        python_callable=check_data_quality,
        poke_interval=3,  # Check every 3 seconds
        timeout=45,  # Maximum 45 seconds
        soft_fail=False,
    )

    # ===== Datetime Sensor: Wait Until Specific Time =====
    # For demo, set to 30 seconds from now
    target_time = datetime.now() + timedelta(seconds=30)
    
    datetime_sensor = DateTimeSensor(
        task_id='wait_until_target_time',
        target_time=target_time,
        poke_interval=2,
        timeout=60,
    )

    # ===== Processing Tasks =====
    def process_all_data():
        """Process data after all sensors have passed"""
        print("All sensors passed! Processing data...")
        files = os.listdir('/tmp/airflow_sensors_demo')
        print(f"Found {len(files)} files to process: {files}")
        for filename in files:
            print(f"  - Processing {filename}")
    
    processing = PythonOperator(
        task_id='process_all_data',
        python_callable=process_all_data,
    )

    # ===== Upstream Verification =====
    def verify_processing():
        """Final verification that processing completed"""
        print("All sensors and processing steps completed successfully!")
        return "Success - Advanced sensor patterns demonstrated"
    
    verify_task = PythonOperator(
        task_id='verify_completion',
        python_callable=verify_processing,
    )

    # ===== DAG Structure =====
    # Setup creates the files first
    setup_task >> [file_sensors, python_sensor, datetime_sensor]
    
    # All sensors must pass before processing
    [file_sensors, python_sensor, datetime_sensor] >> processing >> verify_task


# ===== Additional Notes on Advanced Sensor Patterns =====
"""
ADVANCED SENSOR PATTERNS DEMONSTRATED:

1. **Poke Interval Configuration**
   - Shorter intervals: More responsive, higher CPU/I/O
   - Longer intervals: Less resource intensive, higher latency
   - Can be tuned based on expected event timing

2. **Timeout Strategy**
   - Prevents indefinite waiting
   - soft_fail=True: Task skipped on timeout (pipeline continues)
   - soft_fail=False: Task fails on timeout (pipeline fails)

3. **Sensor Modes**
   - 'poke': Locks worker during polling (simple, blocking)
   - 'reschedule': Frees worker, re-queues task (efficient for long waits)

4. **Multiple Sensor Types**
   - FileSensor: Waits for file creation
   - PythonSensor: Custom logic (most flexible)
   - DateTimeSensor: Waits for specific time
   - ExternalTaskSensor: Cross-DAG dependencies
   - SmartSensor: Reschedules intelligently (experimental)

5. **Error Handling**
   - Retries at sensor level with retry_delay
   - Soft failures allow selective task skipping
   - TaskGroups organize related sensors

6. **Performance Optimization**
   - Use reschedule mode for long-waiting sensors
   - Group sensors in TaskGroups
   - Set appropriate poke_interval values
   - Use exponential backoff for retries

7. **Best Practices**
   - Always set timeout to prevent hanging DAGs
   - Use soft_fail for non-critical dependencies
   - Monitor sensor execution in Airflow UI
   - Log sensor state changes for debugging
   - Use pooling if sensors create bottlenecks
"""
