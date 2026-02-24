# 🚀 Apache Airflow Training - Complete Learning Course

A comprehensive, production-ready Airflow training course with **11 DAGs** progressing from beginner to advanced levels. Perfect for learning Apache Airflow from scratch!

![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.0+-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📚 Overview

This repository contains a **complete learning path** for Apache Airflow with real-world use cases:

- **11 fully functional DAGs** with detailed comments
- **Progressive difficulty**: Beginner → Intermediate → Advanced
- **Ready-to-run examples** in Docker
- **Comprehensive guides** with expected outputs and testing instructions
- **Real-world patterns** and best practices

---

## 🎯 What You'll Learn

### 🟢 Beginner (3 DAGs)
- [x] Creating your first DAG
- [x] Task dependencies and sequential execution
- [x] Parallel task execution

### 🟡 Intermediate (4 DAGs)
- [x] Conditional branching logic
- [x] Error handling and retries
- [x] Multiple operator types
- [x] Sensors and event waiting

### 🔴 Advanced (4 DAGs)
- [x] Dynamic task generation
- [x] Custom operators
- [x] Complex ETL pipelines
- [x] Task groups and workflow organization

---

## 📋 DAG Structure

```
Beginner
├── 01_beginner_hello_world.py              (1 task - Hello World)
├── 02_beginner_sequential_tasks.py         (3 tasks - Extract → Transform → Load)
└── 03_beginner_parallel_tasks.py           (Run 3 tasks simultaneously)

Intermediate
├── 04_intermediate_branching.py            (Conditional branching)
├── 05_intermediate_error_handling.py       (Retries & recovery)
├── 06_intermediate_multiple_operators.py   (Python + Bash operators)
└── 07_intermediate_sensors.py              (Wait for file creation)

Advanced
├── 08_advanced_dynamic_tasks.py            (Generate tasks in loops)
├── 09_advanced_custom_operators.py         (Build your own operators)
├── 10_advanced_complex_etl.py              (Full production ETL)
└── 11_advanced_task_groups.py              (Organize large DAGs)
```

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.8+
- Git

### Setup (5 minutes)

1. **Clone the repository**
   ```bash
   git clone https://github.com/govind-dataengineer/AIRFLOW-TRAINING.git
   cd AIRFLOW-TRAINING
   ```

2. **Start Airflow with Docker**
   ```bash
   docker-compose up -d
   ```

3. **Access Airflow UI**
   ```
   URL: http://localhost:8080
   Username: airflow
   Password: airflow
   ```

4. **Run your first DAG**
   - Find `01_beginner_hello_world` in the DAG list
   - Click the **▶ play button** to trigger it
   - Click the task to see logs
   - Look for: `Hello, Airflow!`

✅ **Done!** You've run your first Airflow DAG!

---

## 📖 Documentation

### Main Guides

1. **[AIRFLOW_LEARNING_GUIDE.md](AIRFLOW_LEARNING_GUIDE.md)** 📚
   - Detailed explanation of each DAG
   - Expected output examples
   - How to test each DAG
   - Real-world use cases
   - Troubleshooting guide

2. **[DAG_QUICK_REFERENCE.md](DAG_QUICK_REFERENCE.md)** ⚡
   - Summary table of all DAGs
   - Learning tracks (Beginner → Intermediate → Advanced)
   - Complexity progression chart
   - Quick commands reference

---

## 🎓 Learning Path (Recommended)

### Week 1: Master the Basics
- **Day 1**: `01_hello_world` (What is a DAG?)
- **Day 2**: `02_sequential_tasks` (How do tasks depend on each other?)
- **Day 3**: `03_parallel_tasks` (How to run tasks together?)

### Week 2: Build Production Skills
- **Day 1**: `04_branching` (Conditional logic)
- **Day 2**: `05_error_handling` (Robust workflows)
- **Day 3**: `06_multiple_operators` (Mix different operators)
- **Day 4**: `07_sensors` (Wait for events)

### Week 3: Advanced Mastery
- **Day 1**: `08_dynamic_tasks` (Scale without hardcoding)
- **Day 2**: `09_custom_operators` (Build domain logic)
- **Day 3**: `10_complex_etl` (Real production pipeline)
- **Day 4**: `11_task_groups` (Organize enterprise DAGs)

---

## 📊 DAG Overview Table

| # | DAG Name | Level | Duration | Key Concepts |
|---|----------|-------|----------|--------------|
| 1 | `01_hello_world` | 🟢 Beginner | ~1s | Basic DAG structure |
| 2 | `02_sequential_tasks` | 🟢 Beginner | ~3s | Dependencies, XCom |
| 3 | `03_parallel_tasks` | 🟢 Beginner | ~2s | Parallelization |
| 4 | `04_branching` | 🟡 Intermediate | ~2s | Conditional execution |
| 5 | `05_error_handling` | 🟡 Intermediate | ~5s | Retries, error recovery |
| 6 | `06_multiple_operators` | 🟡 Intermediate | ~3s | Python, Bash operators |
| 7 | `07_sensors` | 🟡 Intermediate | ~4s | FileSensor, polling |
| 8 | `08_dynamic_tasks` | 🔴 Advanced | ~2s | Loop-based task generation |
| 9 | `09_custom_operators` | 🔴 Advanced | ~2s | Build custom operators |
| 10 | `10_complex_etl` | 🔴 Advanced | ~3s | Full ETL pipeline |
| 11 | `11_task_groups` | 🔴 Advanced | ~3s | Workflow organization |

---

## 🔧 Common Commands

### Docker

```bash
# Start Airflow
docker-compose up -d

# Stop Airflow
docker-compose down

# View logs
docker-compose logs -f webserver

# Restart components
docker-compose restart
```

### Airflow CLI

```bash
# List all DAGs
docker-compose exec airflow-cli airflow dags list

# Trigger a DAG
docker-compose exec airflow-cli airflow dags trigger 01_beginner_hello_world

# Get DAG info
docker-compose exec airflow-cli airflow dags info 01_beginner_hello_world

# List tasks in DAG
docker-compose exec airflow-cli airflow tasks list 02_beginner_sequential_tasks

# View task logs
docker-compose exec airflow-cli airflow tasks logs 01_beginner_hello_world hello_task 2024-01-01
```

### Local Testing

```bash
# Validate DAG syntax
python dags/01_beginner_hello_world.py

# Test task locally
airflow tasks test 01_beginner_hello_world hello_task 2024-01-01
```

---

## 📁 Project Structure

```
AIRFLOW-TRAINING/
├── dags/
│   ├── 01_beginner_hello_world.py
│   ├── 02_beginner_sequential_tasks.py
│   ├── 03_beginner_parallel_tasks.py
│   ├── 04_intermediate_branching.py
│   ├── 05_intermediate_error_handling.py
│   ├── 06_intermediate_multiple_operators.py
│   ├── 07_intermediate_sensors.py
│   ├── 08_advanced_dynamic_tasks.py
│   ├── 09_advanced_custom_operators.py
│   ├── 10_advanced_complex_etl.py
│   ├── 11_advanced_task_groups.py
│   └── __pycache__/
├── config/
├── logs/
├── plugins/
├── docker-compose.yaml
├── .env
├── AIRFLOW_LEARNING_GUIDE.md      ← Detailed guide
├── DAG_QUICK_REFERENCE.md         ← Quick reference
├── README.md                        ← This file
└── .git/
```

---

## 🎯 What Each DAG Teaches

### 01_hello_world ✅
**Purpose**: Verify Airflow installation and understand DAG basics
- Single PythonOperator task
- Basic DAG structure
- How to trigger and monitor

### 02_sequential_tasks ✅
**Purpose**: Learn task dependencies and data passing
- Multiple tasks in order
- Using `>>` operator for dependencies
- XCom for inter-task communication

### 03_parallel_tasks ✅
**Purpose**: Run multiple tasks simultaneously
- Parallel execution patterns
- Performance improvements
- Mixed sequential/parallel workflows

### 04_branching ✅
**Purpose**: Create decision branches in workflows
- BranchPythonOperator
- Conditional task routing
- Multiple execution paths

### 05_error_handling ✅
**Purpose**: Build robust, fault-tolerant DAGs
- Retry mechanisms with backoff
- Error handling and recovery
- SLA monitoring

### 06_multiple_operators ✅
**Purpose**: Combine different operator types
- PythonOperator usage
- BashOperator usage
- Inter-operator communication

### 07_sensors ✅
**Purpose**: Wait for external events
- FileSensor implementation
- Polling mechanisms
- Event-driven workflows

### 08_dynamic_tasks ✅
**Purpose**: Generate tasks dynamically
- Loop-based task creation
- Parameterized tasks
- Scalable workflows

### 09_custom_operators ✅
**Purpose**: Build reusable custom operators
- BaseOperator inheritance
- Custom execution logic
- Operator parameters

### 10_complex_etl ✅
**Purpose**: Production-grade ETL pipeline
- Multi-stage ETL workflow
- Data validation at each stage
- Comprehensive error handling
- Pipeline reporting

### 11_task_groups ✅
**Purpose**: Organize large, complex workflows
- TaskGroup for logical grouping
- Nested hierarchies
- Enterprise-scale organization

---

## ✅ Testing Your DAGs

### Validate Syntax
```bash
python dags/01_beginner_hello_world.py
# No output = syntax OK
```

### Run a DAG in Airflow UI
1. Navigate to http://localhost:8080
2. Find your DAG in the list
3. Click the **▶ play button**
4. Monitor execution
5. Click task to see logs

### Check Logs
```bash
docker-compose logs scheduler | grep "DAG"
docker-compose logs webserver
```

---

## 🐛 Troubleshooting

### DAG doesn't appear in UI
```bash
# Restart scheduler
docker-compose restart scheduler

# Check DAG folder
docker-compose exec airflow-cli airflow config get-value core dags_folder
```

### Import errors
```bash
# Check installed packages
docker-compose exec airflow-cli pip list

# Install missing packages
docker-compose exec airflow-cli pip install pandas numpy
```

### Can't connect to UI
```bash
# Verify containers are running
docker-compose ps

# Check webserver logs
docker-compose logs webserver
```

---

## 📚 Resources

### Official Documentation
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow API Reference](https://airflow.apache.org/api/)
- [Airflow GitHub Repository](https://github.com/apache/airflow)

### Learning Resources
- [Airflow Concepts](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html)
- [Operators and Hooks](https://airflow.apache.org/docs/apache-airflow/stable/operators-and-hooks-ref.html)
- [Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)

### Community
- [Apache Airflow Slack](https://apache-airflow.slack.com/)
- [StackExchange - airflow tag](https://stackoverflow.com/questions/tagged/airflow)
- [GitHub Discussions](https://github.com/apache/airflow/discussions)

---

## 🔄 Git Workflow

### Clone the repo
```bash
git clone https://github.com/govind-dataengineer/AIRFLOW-TRAINING.git
cd AIRFLOW-TRAINING
```

### Create your branch
```bash
git checkout -b feature/your-feature
```

### Push changes
```bash
git add .
git commit -m "Add your changes"
git push origin feature/your-feature
```

---

## 💡 Tips & Best Practices

1. **Always add `catchup=False`** to prevent backfilling
2. **Use meaningful task IDs** - they appear in logs
3. **Add docstrings** with `doc_md` parameter
4. **Set appropriate retries** - balance reliability vs cost
5. **Use XCom carefully** - keep data small
6. **Monitor SLAs** - know your expected completion time
7. **Test locally first** - validate syntax before deployment
8. **Version your DAGs** - treat them like code
9. **Use task groups** - organize complex workflows
10. **Log everything** - helpful for debugging

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Submit a pull request

---

## 👨‍💻 Author

**Govind Singh Bora**
- GitHub: [@govind-dataengineer](https://github.com/govind-dataengineer)
- Repository: [AIRFLOW-TRAINING](https://github.com/govind-dataengineer/AIRFLOW-TRAINING)

---

## ❓ FAQ

**Q: Do I need to modify any DAGs?**
A: No! All DAGs are ready to run immediately. They're designed for learning, not production.

**Q: How long does each DAG take to run?**
A: Most DAGs complete in 1-5 seconds. Check the summary table for details.

**Q: Can I run multiple DAGs at once?**
A: Yes! Airflow scheduler will handle parallelization based on your worker configuration.

**Q: Where's the best place to start?**
A: Start with `01_beginner_hello_world`, then read `AIRFLOW_LEARNING_GUIDE.md` for details.

**Q: How do I create my own DAG?**
A: Use these templates as reference. Start simple, then add complexity.

**Q: Can I use these in production?**
A: These are learning examples. Adapt patterns for your production needs.

---

## 🎉 Next Steps

1. **Run your first DAG**: `01_beginner_hello_world`
2. **Read the guides**: Start with `DAG_QUICK_REFERENCE.md`
3. **Follow the learning path**: 3 weeks to Airflow mastery
4. **Build your own DAG**: Use these as templates
5. **Deploy to production**: Adapt patterns for real workflows

---

**Happy Learning! 🚀**

For detailed information about each DAG, refer to [AIRFLOW_LEARNING_GUIDE.md](AIRFLOW_LEARNING_GUIDE.md)
