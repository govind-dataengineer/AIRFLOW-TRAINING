# 📚 Apache Airflow Learning Journey - Complete DAG Tutorial

Welcome to your Apache Airflow learning path! This guide contains 11 DAGs organized from **Beginner → Intermediate → Advanced** levels with real-world use cases.

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [DAG Overview](#dag-overview)
- [Beginner DAGs](#beginner-dags)
- [Intermediate DAGs](#intermediate-dags)
- [Advanced DAGs](#advanced-dags)
- [How to Run DAGs](#how-to-run-dags)
- [Tips & Tricks](#tips--tricks)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites

Ensure your Airflow is running in Docker:

```bash
cd /Users/govindsinghbora/airflow-training
docker-compose up -d
```

Verify Airflow is running:
```bash
docker-compose logs scheduler | tail -20
```

Access the Web UI:
- **URL**: `http://localhost:8080`
- **Default Username**: `airflow`
- **Default Password**: `airflow`

---

## 📊 DAG Overview

```
BEGINNER (Learn Basics)
├── 01_hello_world              ← Start here!
├── 02_sequential_tasks         ← Dependencies
└── 03_parallel_tasks           ← Parallelization

INTERMEDIATE (Build Skills)
├── 04_branching                ← Conditional logic
├── 05_error_handling           ← Retries & recovery
├── 06_multiple_operators       ← Different task types
└── 07_sensors                  ← Waiting for events

ADVANCED (Master Concepts)
├── 08_dynamic_tasks            ← Loop generation
├── 09_custom_operators         ← Build your own
├── 10_complex_etl              ← Real-world pipeline
└── 11_task_groups              ← Large workflows
```

---

## 🟢 BEGINNER DAGs

### 1️⃣ `01_beginner_hello_world.py`

**📌 Purpose**: Verify Airflow installation and understand basic DAG structure

**🎯 What You'll Learn**:
- How to create a simple DAG
- Basic DAG parameters
- PythonOperator basics
- How to run your first task

**🔧 Key Components**:
```python
- default_args: Default configuration for all tasks
- DAG: The main workflow container
- PythonOperator: Execute Python functions
```

**📝 Expected Output**:
```
Hello, Airflow! This is your first DAG!
Task completed successfully
```

**✅ How to Test**:
1. Go to Airflow UI (http://localhost:8080)
2. Find `01_beginner_hello_world` in the DAG list
3. Click on it and press **Trigger DAG** (play button)
4. Click on the task to see logs
5. Look for "Hello, Airflow!" in the logs

---

### 2️⃣ `02_beginner_sequential_tasks.py`

**📌 Purpose**: Understand task dependencies and data passing between tasks

**🎯 What You'll Learn**:
- Creating multiple tasks
- Defining dependencies with `>>` operator
- XCom (cross-communication) between tasks
- Passing data from one task to another

**🔧 Key Components**:
```python
- extract_task → transform_task → load_task (ETL pipeline)
- XCom methods: xcom_push() and xcom_pull()
- Task instance (ti) parameter
```

**📊 Task Flow**:
```
Extract Data → Transform Data → Load Data
```

**📝 Expected Output**:
```
Extracting data...
Extracted: {'users': ['Alice', 'Bob', 'Charlie'], ...}
Received data: {...}
Transformed: {'users': [...], 'scores': [95, 100, 88]}
Loading data: {...}
Data loaded successfully!
```

**✅ How to Test**:
1. Trigger DAG `02_beginner_sequential_tasks`
2. Wait for all 3 tasks to complete (should take ~3 seconds)
3. Check task logs in order: extract → transform → load
4. Notice how data flows from one task to the next

---

### 3️⃣ `03_beginner_parallel_tasks.py`

**📌 Purpose**: Learn how to run multiple tasks simultaneously

**🎯 What You'll Learn**:
- Parallel task execution
- Performance improvements through parallelization
- Mixed sequential and parallel patterns
- Task grouping strategies

**🔧 Key Components**:
```python
- start >> [process_1, process_2, process_3] >> consolidate
- Three independent batch processors
- Consolidation task combining results
```

**📊 Task Flow**:
```
        ┌─ process_batch_1 ─┐
start ──┤─ process_batch_2 ──┼─ consolidate
        └─ process_batch_3 ─┘
```

**📝 Expected Output**:
```
Starting pipeline...
Processing data batch 1...
Processing data batch 2...
Processing data batch 3...
(All 3 batches run in parallel - faster than sequential!)
Consolidating results...
All batches processed and consolidated
```

**⏱️ Performance**:
- Sequential: ~6 seconds
- Parallel: ~2 seconds (3x faster!)

**✅ How to Test**:
1. Trigger `03_beginner_parallel_tasks`
2. Note the start time
3. Observe all 3 batch processes start ~simultaneously
4. Compare execution time with `02_beginner_sequential_tasks`

---

## 🟡 INTERMEDIATE DAGs

### 4️⃣ `04_intermediate_branching.py`

**📌 Purpose**: Create workflows with conditional logic (if-else branching)

**🎯 What You'll Learn**:
- BranchPythonOperator for conditional execution
- Dynamic task routing
- Multiple execution paths
- Merging branches back together

**🔧 Key Components**:
```python
- BranchPythonOperator: Decides which task runs next
- Low/Medium/High value tasks (3 possible paths)
- trigger_rule='one_success': Allows branches to merge
```

**📊 Task Flow (Random)**:
```
              ┌─ low_value_task
check_value ──┤─ medium_value_task ── final_task
              └─ high_value_task
```

**📝 Expected Output** (Random each run):
```
# Run 1:
Generated value: 25
Route: Low value path
Processing LOW value... (< 33)
Applying discount of 50%

# Run 2:
Generated value: 78
Route: High value path
Processing HIGH value... (> 66)
Applying discount of 10%
```

**✅ How to Test**:
1. Trigger `04_intermediate_branching` multiple times
2. Each run should take a different path
3. Check task logs to see which path was taken
4. Observe how only ONE of the three processing tasks executes

**💡 Real-world Use Case**: 
- Process high-value orders differently
- Route data based on quality scores
- Different handling for different customer types

---

### 5️⃣ `05_intermediate_error_handling.py`

**📌 Purpose**: Handle failures gracefully with retries and error recovery

**🎯 What You'll Learn**:
- Retry mechanisms with backoff
- Error handling and recovery
- Task-level configuration overrides
- Trigger rules (one_success, all_done)
- Service Level Agreements (SLA)

**🔧 Key Components**:
```python
- retries: Number of retry attempts
- retry_delay: Time between retries
- trigger_rule: When task should execute
- try-except blocks for error handling
```

**📝 Expected Output** (for unstable_task):
```
Attempt #1
Task failed on attempt 1. Retrying...
Attempt #2
Task failed on attempt 2. Retrying...
Attempt #3
Success on attempt 3!
```

**✅ How to Test**:
1. Trigger `05_intermediate_error_handling`
2. Watch the unstable_task retry multiple times
3. Notice it eventually succeeds despite failures
4. The cleanup_task runs regardless of success/failure
5. Check SLA configuration in DAG parameters

**💡 Real-world Use Case**:
- API calls that might temporarily fail
- Network requests with temporary issues
- Database operations during maintenance
- Transient infrastructure problems

---

### 6️⃣ `06_intermediate_multiple_operators.py`

**📌 Purpose**: Use different operator types in one DAG (Python, Bash, Email)

**🎯 What You'll Learn**:
- PythonOperator for Python code
- BashOperator for shell commands
- Combining different operator types
- File operations between tasks
- Data passing between operators

**🔧 Key Components**:
```python
- PythonOperator: Execute Python functions
- BashOperator: Execute bash commands
- File I/O: Writing and reading files
```

**📊 Task Flow**:
```
python_task_1 → bash_task → python_task_2 → bash_cleanup
(write file)    (read file)  (read file)    (delete file)
```

**📝 Expected Output**:
```
Executing Python function
Hello from Bash
[date output]
This is output from Python task
Read from file: This is output from Python task
Cleanup completed
```

**✅ How to Test**:
1. Trigger `06_intermediate_multiple_operators`
2. Watch different operators execute in sequence
3. Verify file is created by Python, read by Bash, then cleaned up
4. Check logs for output at each stage

**💡 Real-world Use Case**:
- Python for data processing, Bash for system commands
- Database operations via Python, log analysis via Bash
- Mixed team expertise (Python devs, DevOps engineers)

---

### 7️⃣ `07_intermediate_sensors.py`

**📌 Purpose**: Wait for external events or conditions

**🎯 What You'll Learn**:
- FileSensor for file-based triggers
- Polling mechanisms
- Waiting for external events
- Sensor timeouts
- Task coordination

**🔧 Key Components**:
```python
- FileSensor: Waits for file to appear
- poke_interval: How often to check (2 seconds)
- timeout: Max wait time (60 seconds)
```

**📊 Task Flow**:
```
create_marker_file → wait_for_data_file (sensor waits...) → process_file
                     (polls every 2 seconds)
```

**📝 Expected Output**:
```
Creating marker file: /tmp/airflow_demo/data_ready.txt
Marker file created successfully
(Sensor starts polling...)
[After ~2 seconds when file is detected]
Contents of marker file:
Data is ready for processing
Created at: 2026-02-24 XX:XX:XX
Processing file...
```

**⏱️ Timing**:
- File creation: ~2 seconds
- Sensor detection: ~2 seconds
- Total: ~4 seconds

**✅ How to Test**:
1. Trigger `07_intermediate_sensors`
2. Observe the sensor task polling
3. Task completes when file is detected
4. Check `/tmp/airflow_demo/data_ready.txt`

**💡 Real-world Use Case**:
- Waiting for daily data files from partners
- Monitoring S3 buckets for new data
- Waiting for scheduled processes to complete
- File-based data exchange systems

---

## 🔴 ADVANCED DAGs

### 8️⃣ `08_advanced_dynamic_tasks.py`

**📌 Purpose**: Generate tasks dynamically based on data

**🎯 What You'll Learn**:
- Creating tasks in a loop
- Dynamic parallelization
- Scalable workflows for variable amounts of data
- Processing collections of items
- Grid pattern execution

**🔧 Key Components**:
```python
- Loop to generate multiple tasks
- Parametrized tasks using op_kwargs
- Dynamic task naming
- Scaling from 5 to 1000+ tasks
```

**📊 Task Flow**:
```
start → process_item_a ──┐
     → process_item_b ───┼─ aggregate_results
     → process_item_c ───┤
     → process_item_d ───┤
     → process_item_e ──┘
```

**📝 Expected Output**:
```
Processing items dynamically
Processing: item_a
Result: {'item': 'item_a', 'processed_at': '...', 'status': 'completed'}
[... similar for item_b, c, d, e ...]
Aggregating results from all items...
Number of items processed: 5
Items: ['item_a', 'item_b', 'item_c', 'item_d', 'item_e']
```

**✅ How to Test**:
1. Trigger `08_advanced_dynamic_tasks`
2. Observe 5 dynamic process_item_* tasks execute in parallel
3. Check task names: `process_item_a`, `process_item_b`, etc.
4. Edit ITEMS_TO_PROCESS list to change number of tasks

**⚡ Scalability**:
- Change `ITEMS_TO_PROCESS = ['item_a', ... 'item_z']` for 26 tasks
- Same pattern works for 1000+ items
- Airflow handles scheduling automatically

**💡 Real-world Use Case**:
- Processing files for multiple regions
- Running queries for multiple databases
- Sending emails to multiple customers
- Parallel processing without hardcoding task count

---

### 9️⃣ `09_advanced_custom_operators.py`

**📌 Purpose**: Create reusable custom operators for domain-specific logic

**🎯 What You'll Learn**:
- Custom operator design patterns
- Inheritance from BaseOperator
- Operator parameters and configuration
- Custom execute() logic
- Reusability across DAGs

**🔧 Key Components**:
```python
- DataValidationOperator: Custom validation logic
- DataTransformOperator: Custom transformation logic
- Operator initialization with parameters
- UI customization (colors)
```

**📝 Expected Output**:
```
Validating data: {'name': 'john', 'email': 'john@example.com', 'age': 30}
INFO - Validation successful!
Transforming data with type: uppercase
INFO - Transformation result: {'name': 'JOHN', 'email': 'JOHN@EXAMPLE.COM', 'age': 30}
Custom operators demo complete
```

**✅ How to Test**:
1. Trigger `09_advanced_custom_operators`
2. Observe both custom operators execute
3. Check logs for validation and transformation steps
4. Note the custom operators appear in UI with custom colors

**🔨 Creating Your Own Operator**:

```python
from airflow.models import BaseOperator

class MyCustomOperator(BaseOperator):
    @apply_defaults
    def __init__(self, my_param, *args, **kwargs):
        super(MyCustomOperator, self).__init__(*args, **kwargs)
        self.my_param = my_param
    
    def execute(self, context):
        # Your logic here
        pass
```

**💡 Real-world Use Case**:
- Domain-specific transformations
- Company-internal validation rules
- Custom database connectors
- Proprietary business logic

---

### 🔟 `10_advanced_complex_etl.py`

**📌 Purpose**: Production-grade ETL pipeline with full validation

**🎯 What You'll Learn**:
- Multi-stage ETL (Extract, Transform, Load)
- Data quality checks at each stage
- Error handling throughout pipeline
- Transaction management
- Comprehensive logging and reporting

**🔧 Key Components**:
```python
- Extract: Read from source (5 employees)
- Validate Extract: Check data integrity
- Transform: Add calculated columns, enrich data
- Validate Transform: Verify transformations
- Load: Write to warehouse
- Validate Load: Confirm successful load
- Report: Generate summary statistics
```

**📊 Task Flow**:
```
Extract → Validate → Transform → Validate → Load → Validate → Report
```

**📝 Expected Output**:
```
🔍 EXTRACT: Reading from source...
✅ Extracted 5 records

🔍 VALIDATE EXTRACT: Checking data quality...
✅ Validation passed: 5 records verified

🔄 TRANSFORM: Processing data...
✅ Transformed 5 records
   - Added salary_with_bonus column
   - Added salary_bracket column
   - Added name_upper column

🔍 VALIDATE TRANSFORM: Checking transformations...
✅ Transformation validation passed

📊 LOAD: Writing to warehouse...
✅ Loaded 5 records to warehouse

🔍 VALIDATE LOAD: Checking warehouse data...
✅ Load validation passed

📋 PIPELINE REPORT:
{
  "pipeline_status": "SUCCESS",
  "total_records": 5,
  "timestamp": "2026-02-24T...",
  "departments": ["Engineering", "Sales", "Management"],
  "avg_salary": 56400,
  "avg_salary_with_bonus": 62040
}
```

**✅ How to Test**:
1. Trigger `10_advanced_complex_etl`
2. Monitor all 7 tasks complete in sequence
3. Observe validation at each stage
4. Check the final report with statistics
5. Verify no records are lost during pipeline

**⚠️ Error Scenarios to Test**:
- Try modifying data to fail validation
- Check how pipeline handles errors
- Review error messages in logs

**💡 Real-world Use Case**:
- Daily sales data ETL
- Customer information synchronization
- Financial data reconciliation
- Data warehouse loading

---

### 1️⃣1️⃣ `11_advanced_task_groups.py`

**📌 Purpose**: Organize large, complex workflows using TaskGroups

**🎯 What You'll Learn**:
- TaskGroup for logical organization
- Nested workflow structures
- Improved DAG visualization
- Hierarchical task management
- Enterprise-scale workflow design

**🔧 Key Components**:
```python
- data_preparation: 3 tasks for data prep
- model_training: 3 tasks for model training
- deployment: 3 tasks for deployment
- Each group has internal dependencies
- Groups have cross-group dependencies
```

**📊 Task Flow with TaskGroups**:
```
start
  ↓
[data_preparation]
  ├─ preprocess
  ├─ feature_engineering (after preprocess)
  └─ validate_features (after feature_eng)
      ↓
[model_training]
  ├─ train_model
  ├─ evaluate_model (after train)
  └─ test_model (after train)
      ↓
[deployment]
  ├─ deploy_model
  ├─ notify_stakeholders (after deploy)
  └─ log_metrics (after notify)
      ↓
end
```

**📝 Expected Output**:
```
🚀 Starting ML pipeline

📋 Running preprocessing...
  - Cleaning data
  - Handling missing values

🔧 Feature engineering...
  - Creating new features
  - Scaling features

✅ Validating features...

🤖 Training machine learning model...
  - Training on dataset
  - Model accuracy: 0.95

📊 Evaluating model...
  - Precision: 0.92
  - Recall: 0.93
  - F1-Score: 0.925

🧪 Testing model on test set...
  - Test accuracy: 0.94

🚀 Deploying model to production...
  - Model deployed successfully

📧 Notifying stakeholders...
  - Email sent to ML team
  - Email sent to product team

📈 Logging metrics...
  - Metrics saved to monitoring system

✅ ML pipeline completed
```

**✅ How to Test**:
1. Trigger `11_advanced_task_groups`
2. In Airflow UI, expand each TaskGroup to see nested tasks
3. Observe auto-generated intermediate tasks (group.downstream_list_task)
4. Monitor task execution in correct order
5. Compare DAG visualization with/without groups

**📊 Visualization Benefits**:
- Collapsed view shows only groups
- Expanded view shows all tasks
- Cleaner graph for large DAGs
- Easier to understand workflow logic

**💡 Real-world Use Case**:
- ML pipeline organization
- Multi-stage data processing
- Separate teams working on different groups
- Large enterprise workflows (100+ tasks)

---

## 🎮 How to Run DAGs

### Method 1: Using Airflow Web UI (Easiest)

1. **Access Airflow UI**
   ```
   http://localhost:8080
   2. **Find your DAG** in the DAG list
   3. **Trigger the DAG** by clicking the play button (▶)
   4. **Monitor execution**
      - Refresh page to see status
      - Click task to see logs
      - Check success/failure status

### Method 2: Using Airflow CLI

```bash
# List all DAGs
docker-compose exec airflow-cli airflow dags list

# Trigger a specific DAG
docker-compose exec airflow-cli airflow dags trigger 01_beginner_hello_world

# Get DAG info
docker-compose exec airflow-cli airflow dags info 01_beginner_hello_world

# View DAG code
docker-compose exec airflow-cli airflow dags code 01_beginner_hello_world

# List tasks in a DAG
docker-compose exec airflow-cli airflow tasks list 01_beginner_hello_world
```

### Method 3: Direct Python Import (For Testing)

```python
import sys
sys.path.insert(0, '/Users/govindsinghbora/airflow-training/dags')
from dags/01_beginner_hello_world import dag

# This won't work - DAGs are loaded by Airflow scheduler
```

---

## 💡 Tips & Tricks

### 1. **Check DAG Syntax**
```bash
cd /Users/govindsinghbora/airflow-training/dags
python -m py_compile 01_beginner_hello_world.py
# No output = OK; errors = syntax issues
```

### 2. **View DAG Logs**
```bash
# View DAG parsing logs
docker-compose logs scheduler | grep \"DAG\"

# View specific task logs
docker-compose exec airflow-cli airflow tasks logs 01_beginner_hello_world hello_task 2024-01-01
```

### 3. **Enable DAG File Processing**
```bash
# Check if dags folder is being scanned
docker-compose exec airflow-cli airflow config get-value core dags_folder
# Should be: /root/airflow/dags or similar
```

### 4. **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| DAG not appearing | Restart scheduler: `docker-compose restart scheduler` |
| Import errors | Check dependencies: `pip list \\| grep pandas` |
| Task fails | Check logs: Click task → See error details |
| Port 8080 busy | `lsof -i :8080` and kill process |
| File not found | Use `/opt/airflow/dags/` inside Docker |

### 5. **Test Your DAG Locally**
```bash
# Validate DAG syntax
python 01_beginner_hello_world.py

# Test task execution
airflow tasks test 01_beginner_hello_world hello_task 2024-01-01
```

---

## 📚 Learning Path (Recommended Order)

### Week 1: Beginner Basics
- Day 1: `01_hello_world` - Just run it!
- Day 2: `02_sequential_tasks` - Understand dependencies
- Day 3: `03_parallel_tasks` - Learn parallelization

### Week 2: Intermediate Concepts
- Day 1: `04_branching` - Try different values
- Day 2: `05_error_handling` - Simulate failures
- Day 3: `06_multiple_operators` - Mix operators
- Day 4: `07_sensors` - Wait for events

### Week 3: Advanced Mastery
- Day 1: `08_dynamic_tasks` - Change item count
- Day 2: `09_custom_operators` - Build your own
- Day 3: `10_complex_etl` - Real production pipeline
- Day 4: `11_task_groups` - Organize large DAGs

---

## ❓ Troubleshooting

### DAG doesn't appear in UI
```bash
# Restart Airflow components
docker-compose restart

# Check scheduler logs
docker-compose logs scheduler | tail -50

# Verify DAG syntactic validity
python /path/to/dag.py
```

### Task fails with import error
```bash
# Install missing packages
docker-compose exec airflow-worker pip install pandas numpy

# Or add to requirements.txt and rebuild
```

### Can't connect to Airflow UI
```bash
# Check if containers are running
docker-compose ps

# View container logs
docker-compose logs webserver
```

### Tasks not executing in parallel
```bash
# Check parallelism settings in airflow.cfg
# Ensure enough workers are running
docker-compose ps
```

---

## 🎓 Next Steps

After completing all DAGs:

1. **Modify existing DAGs** - Change schedules, add tasks, experiment
2. **Build your own DAG** - Use these as templates
3. **Explore Additional Operators**:
   - SqlOperator for databases
   - S3Operator for AWS
   - EmailOperator for notifications
   - DockerOperator for containerized tasks

4. **Deploy to Production** - Set up Airflow cluster
5. **Monitor & Alert** - Set up SLAs and notifications
6. **Join Community** - Apache Airflow Slack, GitHub

---

## 📞 Support

For issues or questions:
- Check Airflow logs: `docker-compose logs`
- Visit [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- Community support: [Airflow Slack](https://apache-airflow.slack.com/)

---

**Happy Learning! 🚀**

Last Updated: 2026-02-24
"