"""
ADVANCED: TaskGroup for Organizing Complex Workflows
Tags: ['advanced', 'task-group', 'workflow-organization']

This DAG demonstrates:
- Using TaskGroup to organize related tasks
- Nested workflow structures
- Cleaner DAG visualization
- Grouping tasks by business logic

Key Concepts:
- TaskGroup for logical grouping
- Nested task hierarchies
- Better DAG readability
- Organizing large workflows
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

# Task functions
def preprocessing_step():
    print(\"📋 Running preprocessing...\")
    print(\"  - Cleaning data\")\n    print(\"  - Handling missing values\")\n\ndef feature_engineering_step():\n    print(\"🔧 Feature engineering...\")\n    print(\"  - Creating new features\")\n    print(\"  - Scaling features\")\n\ndef validation_step():\n    print(\"✅ Validating features...\")\n\ndef train_model():\n    print(\"🤖 Training machine learning model...\")\n    print(\"  - Training on dataset\")\n    print(\"  - Model accuracy: 0.95\")\n\ndef evaluate_model():\n    print(\"📊 Evaluating model...\")\n    print(\"  - Precision: 0.92\")\n    print(\"  - Recall: 0.93\")\n    print(\"  - F1-Score: 0.925\")\n\ndef test_model():\n    print(\"🧪 Testing model on test set...\")\n    print(\"  - Test accuracy: 0.94\")\n\ndef deploy_model():\n    print(\"🚀 Deploying model to production...\")\n    print(\"  - Model deployed successfully\")\n\ndef notify_stakeholders():\n    print(\"📧 Notifying stakeholders...\")\n    print(\"  - Email sent to ML team\")\n    print(\"  - Email sent to product team\")\n\ndef log_metrics():\n    print(\"📈 Logging metrics...\")\n    print(\"  - Metrics saved to monitoring system\")\n\n# Create the DAG\nwith DAG(\n    dag_id='11_advanced_task_groups',\n    default_args=default_args,\n    description='DAG using TaskGroups for organization',\n    schedule_interval='@daily',\n    catchup=False,\n    tags=['advanced', 'task-group', 'ml-pipeline'],\n) as dag:\n    \n    start = PythonOperator(\n        task_id='start_pipeline',\n        python_callable=lambda: print(\"🚀 Starting ML pipeline\"),\n    )\n    \n    # Task Group 1: Data Preparation\n    with TaskGroup('data_preparation') as data_prep:\n        preprocess = PythonOperator(\n            task_id='preprocess',\n            python_callable=preprocessing_step,\n        )\n        \n        feature_eng = PythonOperator(\n            task_id='feature_engineering',\n            python_callable=feature_engineering_step,\n        )\n        \n        validate = PythonOperator(\n            task_id='validate_features',\n            python_callable=validation_step,\n        )\n        \n        # Task dependencies within group\n        preprocess >> feature_eng >> validate\n    \n    # Task Group 2: Model Training\n    with TaskGroup('model_training') as model_train:\n        train = PythonOperator(\n            task_id='train_model',\n            python_callable=train_model,\n        )\n        \n        evaluate = PythonOperator(\n            task_id='evaluate_model',\n            python_callable=evaluate_model,\n        )\n        \n        test = PythonOperator(\n            task_id='test_model',\n            python_callable=test_model,\n        )\n        \n        # Task dependencies within group\n        train >> [evaluate, test]\n    \n    # Task Group 3: Deployment & Monitoring\n    with TaskGroup('deployment') as deployment:\n        deploy = PythonOperator(\n            task_id='deploy_model',\n            python_callable=deploy_model,\n        )\n        \n        notify = PythonOperator(\n            task_id='notify_stakeholders',\n            python_callable=notify_stakeholders,\n        )\n        \n        log_metrics_task = PythonOperator(\n            task_id='log_metrics',\n            python_callable=log_metrics,\n        )\n        \n        # Task dependencies within group\n        deploy >> notify >> log_metrics_task\n    \n    end = PythonOperator(\n        task_id='end_pipeline',\n        python_callable=lambda: print(\"✅ ML pipeline completed\"),\n    )\n    \n    # Cross-group dependencies\n    start >> data_prep >> model_train >> deployment >> end\n"