"""
ADVANCED: Complex ETL Pipeline with Data Validation
Tags: ['advanced', 'etl', 'data-pipeline', 'validation']

This DAG demonstrates:
- Complex ETL workflow (Extract, Transform, Load)
- Data validation at each stage
- Exception handling
- Checkpoints and data quality checks

Key Concepts:
- Multi-stage ETL pipeline
- Data quality validation
- Error handling throughout pipeline
- Logging and monitoring
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import pandas as pd

default_args = {
    'owner': 'data-engineering',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 1, 1),
}

# Simulated data storage
DATA_STORE = {}

def extract_from_source():
    """Extract data from source"""
    print("🔍 EXTRACT: Reading from source...")
    
    source_data = [
        {'id': 1, 'name': 'Alice', 'salary': 50000, 'department': 'Engineering'},
        {'id': 2, 'name': 'Bob', 'salary': 60000, 'department': 'Sales'},
        {'id': 3, 'name': 'Charlie', 'salary': 55000, 'department': 'Engineering'},
        {'id': 4, 'name': 'Diana', 'salary': 65000, 'department': 'Management'},
        {'id': 5, 'name': 'Eve', 'salary': 52000, 'department': 'Sales'},
    ]
    
    DATA_STORE['raw'] = source_data
    print(f"✅ Extracted {len(source_data)} records")
    return len(source_data)

def validate_extract(ti):
    """Validate extracted data"""
    print("🔍 VALIDATE EXTRACT: Checking data quality...")
    
    data = DATA_STORE.get('raw', [])
    
    # Validation checks
    assert len(data) > 0, "No data extracted"
    assert all('id' in record for record in data), "Missing 'id' field"
    assert all('name' in record for record in data), "Missing 'name' field"
    assert all('salary' in record for record in data), "Missing 'salary' field"
    
    # Check for duplicates
    ids = [record['id'] for record in data]
    assert len(ids) == len(set(ids)), "Duplicate IDs found"
    
    # Check salary values
    assert all(record['salary'] > 0 for record in data), "Invalid salary values"
    
    print(f"✅ Validation passed: {len(data)} records verified")
    return True

def transform_data(ti):
    """Transform the data"""
    print("🔄 TRANSFORM: Processing data...")
    
    raw_data = DATA_STORE.get('raw', [])
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(raw_data)
    
    # Transformations
    df['salary_with_bonus'] = df['salary'] * 1.1  # Add 10% bonus
    df['salary_bracket'] = df['salary'].apply(
        lambda x: 'Senior' if x > 60000 else ('Mid' if x > 50000 else 'Junior')
    )
    df['name_upper'] = df['name'].str.upper()
    
    # Store transformed data
    DATA_STORE['transformed'] = df.to_dict('records')\n    print(f\"✅ Transformed {len(df)} records\")\n    print(f\"   - Added salary_with_bonus column\")\n    print(f\"   - Added salary_bracket column\")\n    print(f\"   - Added name_upper column\")\n    return len(df)\n\ndef validate_transform(ti):\n    \"\"\"Validate transformed data\"\"\"\n    print(\"🔍 VALIDATE TRANSFORM: Checking transformations...\")\n    \n    data = DATA_STORE.get('transformed', [])\n    \n    # Validation checks\n    assert len(data) > 0, \"No transformed data\"\n    assert all('salary_with_bonus' in record for record in data), \"Missing salary_with_bonus\"\n    assert all('salary_bracket' in record for record in data), \"Missing salary_bracket\"\n    assert all(record['salary_with_bonus'] > record['salary'] for record in data), \"Bonus calculation error\"\n    \n    print(f\"✅ Transformation validation passed\")\n    return True\n\ndef load_to_warehouse():\n    \"\"\"Load data to warehouse\"\"\"\n    print(\"📊 LOAD: Writing to warehouse...\")\n    \n    transformed_data = DATA_STORE.get('transformed', [])\n    \n    # Simulate loading to warehouse\n    DATA_STORE['warehouse'] = {\n        'table': 'employees',\n        'records': len(transformed_data),\n        'timestamp': datetime.now().isoformat(),\n        'data': transformed_data\n    }\n    \n    print(f\"✅ Loaded {len(transformed_data)} records to warehouse\")\n    return True\n\ndef validate_load(ti):\n    \"\"\"Validate loaded data\"\"\"\n    print(\"🔍 VALIDATE LOAD: Checking warehouse data...\")\n    \n    warehouse_data = DATA_STORE.get('warehouse', {})\n    \n    assert 'table' in warehouse_data, \"Missing table info\"\n    assert 'records' in warehouse_data, \"Missing record count\"\n    assert warehouse_data['records'] > 0, \"No records loaded\"\n    \n    print(f\"✅ Load validation passed\")\n    return True\n\ndef generate_report(ti):\n    \"\"\"Generate pipeline execution report\"\"\"\n    print(\"📈 REPORT: Generating pipeline report...\")\n    \n    warehouse_data = DATA_STORE.get('warehouse', {})\n    transformed_data = DATA_STORE.get('transformed', [])\n    \n    report = {\n        'pipeline_status': 'SUCCESS',\n        'total_records': len(transformed_data),\n        'timestamp': datetime.now().isoformat(),\n        'departments': list(set(r['department'] for r in transformed_data)),\n        'avg_salary': sum(r['salary'] for r in transformed_data) / len(transformed_data),\n        'avg_salary_with_bonus': sum(r['salary_with_bonus'] for r in transformed_data) / len(transformed_data),\n    }\n    \n    print(f\"\\n📋 PIPELINE REPORT:\")\n    print(json.dumps(report, indent=2))\n    return report\n\n# Create the DAG\nwith DAG(\n    dag_id='10_advanced_complex_etl',\n    default_args=default_args,\n    description='Complex ETL pipeline with validation',\n    schedule_interval='@daily',\n    catchup=False,\n    tags=['advanced', 'etl', 'data-pipeline'],\n) as dag:\n    \n    # EXTRACT phase\n    extract = PythonOperator(\n        task_id='extract_data',\n        python_callable=extract_from_source,\n        doc_md=\"Extract data from source system\"\n    )\n    \n    validate_extract_task = PythonOperator(\n        task_id='validate_extract',\n        python_callable=validate_extract,\n        doc_md=\"Validate extracted data quality\"\n    )\n    \n    # TRANSFORM phase\n    transform = PythonOperator(\n        task_id='transform_data',\n        python_callable=transform_data,\n        doc_md=\"Transform and enrich data\"\n    )\n    \n    validate_transform_task = PythonOperator(\n        task_id='validate_transform',\n        python_callable=validate_transform,\n        doc_md=\"Validate transformed data\"\n    )\n    \n    # LOAD phase\n    load = PythonOperator(\n        task_id='load_to_warehouse',\n        python_callable=load_to_warehouse,\n        doc_md=\"Load data to warehouse\"\n    )\n    \n    validate_load_task = PythonOperator(\n        task_id='validate_load',\n        python_callable=validate_load,\n        doc_md=\"Validate loaded data\"\n    )\n    \n    # REPORTING phase\n    report = PythonOperator(\n        task_id='generate_report',\n        python_callable=generate_report,\n        doc_md=\"Generate pipeline execution report\"\n    )\n    \n    # Pipeline orchestration\n    # Extract -> Validate Extract -> Transform -> Validate Transform -> Load -> Validate Load -> Report\n    extract >> validate_extract_task >> transform >> validate_transform_task >> load >> validate_load_task >> report\n"