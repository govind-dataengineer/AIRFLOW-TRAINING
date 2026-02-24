"""
ADVANCED: Custom Operators and Hooks
Tags: ['advanced', 'custom-operator', 'hooks']

This DAG demonstrates:
- Creating and using custom Python classes as operators
- Operator inheritance
- Custom logic in operators

Key Concepts:
- Creating a custom operator class
- Overriding execute method
- Custom operator parameters
- Reusable operator components
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from datetime import datetime, timedelta
import json

# Custom Operator Class
class DataValidationOperator(BaseOperator):
    """
    Custom operator that validates data structure
    
    :param data: The data to validate
    :param schema: Expected data structure
    """
    
    template_fields = ['data']
    ui_color = '#e74c3c'  # Red color in UI
    
    @apply_defaults
    def __init__(self,
                 data=None,
                 schema=None,
                 *args,
                 **kwargs):
        super(DataValidationOperator, self).__init__(*args, **kwargs)
        self.data = data
        self.schema = schema
    
    def execute(self, context):
        """Execute the validation"""
        self.log.info(f"Validating data: {self.data}")
        
        if self.schema:
            # Check if all schema keys are present in data
            missing_keys = set(self.schema) - set(self.data.keys())
            if missing_keys:
                raise ValueError(f"Missing keys in data: {missing_keys}")
            
            # Check if all values are of correct type
            for key, expected_type in self.schema.items():
                if not isinstance(self.data[key], expected_type):
                    raise TypeError(f"Key '{key}' should be {expected_type.__name__}, got {type(self.data[key]).__name__}")
        
        self.log.info("Validation successful!")
        return {"status": "validated", "data": self.data}

# Another custom operator
class DataTransformOperator(BaseOperator):
    """Custom operator for data transformation"""
    
    template_fields = ['input_data']
    ui_color = '#3498db'  # Blue color in UI
    
    @apply_defaults
    def __init__(self,
                 input_data=None,
                 transformation_type='uppercase',
                 *args,
                 **kwargs):
        super(DataTransformOperator, self).__init__(*args, **kwargs)
        self.input_data = input_data
        self.transformation_type = transformation_type
    
    def execute(self, context):
        self.log.info(f"Transforming data with type: {self.transformation_type}")
        
        if self.transformation_type == 'uppercase':
            result = {k: v.upper() if isinstance(v, str) else v 
                     for k, v in self.input_data.items()}
        elif self.transformation_type == 'double':
            result = {k: v * 2 if isinstance(v, (int, float)) else v 
                     for k, v in self.input_data.items()}
        else:
            result = self.input_data
        
        self.log.info(f"Transformation result: {result}")
        return result

# Create the DAG
with DAG(
    dag_id='09_advanced_custom_operators',
    default_args={'owner': 'airflow', 'start_date': datetime(2024, 1, 1)},
    description='DAG using custom operators',
    schedule_interval='@daily',
    catchup=False,
    tags=['advanced', 'custom-operator'],
) as dag:
    
    start = PythonOperator(
        task_id='start',
        python_callable=lambda: print("Starting custom operator demo"),
    )
    
    # Using custom validation operator
    sample_data = {
        'name': 'john',
        'email': 'john@example.com',
        'age': 30
    }
    
    schema = {
        'name': str,
        'email': str,
        'age': int
    }
    
    validate = DataValidationOperator(
        task_id='validate_data',
        data=sample_data,
        schema=schema,
        doc_md="Validate data structure"
    )
    
    # Using custom transform operator
    transform = DataTransformOperator(
        task_id='transform_data',
        input_data=sample_data,
        transformation_type='uppercase',
        doc_md="Transform data to uppercase"
    )
    
    end = PythonOperator(
        task_id='end',
        python_callable=lambda: print("Custom operators demo complete"),
    )
    
    # Dependencies
    start >> validate >> transform >> end
