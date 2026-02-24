# 🗂️ Airflow DAGs - Quick Reference

## 📊 DAG Summary Table

| # | DAG ID | Level | Tags | Duration | Concepts | Status |
|---|--------|-------|------|----------|----------|--------|
| 1️⃣ | `01_beginner_hello_world` | 🟢 BEGINNER | `hello-world` | ~1s | Basic DAG, Single task | ✅ Ready |
| 2️⃣ | `02_beginner_sequential_tasks` | 🟢 BEGINNER | `dependencies, etl` | ~3s | Task order, XCom, ETL | ✅ Ready |
| 3️⃣ | `03_beginner_parallel_tasks` | 🟢 BEGINNER | `parallel` | ~2s | Parallelization, Speed | ✅ Ready |
| 4️⃣ | `04_intermediate_branching` | 🟡 INTERMEDIATE | `branching, conditional` | ~2s | Branch logic, if-else | ✅ Ready |
| 5️⃣ | `05_intermediate_error_handling` | 🟡 INTERMEDIATE | `error-handling, retries` | ~5s | Retries, SLA, Recovery | ✅ Ready |
| 6️⃣ | `06_intermediate_multiple_operators` | 🟡 INTERMEDIATE | `multiple-operators, bash` | ~3s | Python + Bash, Files | ✅ Ready |
| 7️⃣ | `07_intermediate_sensors` | 🟡 INTERMEDIATE | `sensors, file-ops` | ~4s | FileSensor, Polling | ✅ Ready |
| 8️⃣ | `08_advanced_dynamic_tasks` | 🔴 ADVANCED | `dynamic-tasks` | ~2s | Loop tasks, Scaling | ✅ Ready |
| 9️⃣ | `09_advanced_custom_operators` | 🔴 ADVANCED | `custom-operator` | ~2s | Build operators, Reuse | ✅ Ready |
| 🔟 | `10_advanced_complex_etl` | 🔴 ADVANCED | `etl, data-pipeline` | ~3s | Full ETL, Validation | ✅ Ready |
| 1️⃣1️⃣ | `11_advanced_task_groups` | 🔴 ADVANCED | `task-group, ml` | ~3s | Organization, Groups | ✅ Ready |

---

## 🎯 Learning Tracks

### 🟢 BEGINNER TRACK (3 DAGs)
Learn the absolute basics of Airflow

```
START HERE
    ↓
01_hello_world         (What is a DAG?)
    ↓
02_sequential_tasks    (How do tasks depend on each other?)
    ↓
03_parallel_tasks      (How to run tasks together?)
    ↓
READY FOR: Learn task operators
```

### 🟡 INTERMEDIATE TRACK (4 DAGs)
Build production-ready workflows

```
Prerequisites: Complete BEGINNER track
    ↓
04_branching           (What if I need conditions?)
    ↓
05_error_handling      (What if something fails?)
    ↓
06_multiple_operators  (Can I mix different task types?)
    ↓
07_sensors             (Can I wait for external events?)
    ↓
READY FOR: Advanced patterns
```

### 🔴 ADVANCED TRACK (4 DAGs)
Master complex enterprise workflows

```
Prerequisites: Complete INTERMEDIATE track
    ↓
08_dynamic_tasks       (Can I create tasks dynamically?)
    ↓
09_custom_operators    (Can I build my own operators?)
    ↓
10_complex_etl         (Put it all together - real ETL)
    ↓
11_task_groups         (How do I organize huge DAGs?)
    ↓
READY FOR: Production deployments!
```

---

## 🚀 Quick Start: Running Your First DAG

### Step 1: Start Airflow
```bash
cd /Users/govindsinghbora/airflow-training
docker-compose up -d
```

### Step 2: Access Web UI
```
http://localhost:8080
Username: airflow
Password: airflow
```

### Step 3: Find & Run DAG
1. Find `01_beginner_hello_world` in the DAG list
2. Click the **play button** (▶) to trigger it
3. Wait ~2 seconds
4. Click on the task to see logs
5. Look for: `Hello, Airflow! This is your first DAG!`

✅ **Congratulations! You've run your first Airflow DAG!**

---

## 📈 Complexity Progression

```
01_hello_world                 0.0
02_sequential_tasks            0.2
03_parallel_tasks              0.3
  ↓
04_branching                   0.4
05_error_handling              0.5
06_multiple_operators          0.6
07_sensors                     0.7
  ↓
08_dynamic_tasks               0.8
09_custom_operators            0.9
10_complex_etl                 0.95
11_task_groups                 1.0 ← Master of Airflow!
```

---

## 🔑 Key Concepts by DAG

### DAG Structure
- `01_hello_world` ← How DAGs are defined

### Task Execution
- `02_sequential_tasks` ← Order of execution
- `03_parallel_tasks` ← Concurrent execution
- `04_branching` ← Conditional execution

### Task Communication
- `02_sequential_tasks` ← XCom between tasks
- `10_complex_etl` ← Data passing stages

### Error Handling
- `05_intermediate_error_handling` ← Retries & recovery
- `10_complex_etl` ← Try-catch patterns

### Operators
- `06_multiple_operators` ← Different operator types
- `09_custom_operators` ← Build your own

### Advanced Features
- `07_sensors` ← Wait for events
- `08_dynamic_tasks` ← Generate tasks dynamically
- `11_task_groups` ← Organize workflows

---

## 🎮 Common Tasks

### \"I want to understand how DAGs work\"
→ Start with `01_hello_world` and `02_sequential_tasks`

### \"I want to learn error handling\"
→ Study `05_intermediate_error_handling`

### \"I want to build a production pipeline\"
→ Follow `10_advanced_complex_etl`

### \"I want to organize a huge DAG\"
→ Learn `11_advanced_task_groups`

### \"I need to process multiple items\"
→ Use pattern from `08_advanced_dynamic_tasks`

### \"I want custom business logic\"
→ Build your own like `09_advanced_custom_operators`

---

## 📋 File Locations

All DAGs are in:
```
/Users/govindsinghbora/airflow-training/dags/
├── 01_beginner_hello_world.py
├── 02_beginner_sequential_tasks.py
├── 03_beginner_parallel_tasks.py
├── 04_intermediate_branching.py
├── 05_intermediate_error_handling.py
├── 06_intermediate_multiple_operators.py
├── 07_intermediate_sensors.py
├── 08_advanced_dynamic_tasks.py
├── 09_advanced_custom_operators.py
├── 10_advanced_complex_etl.py
├── 11_advanced_task_groups.py
├── AIRFLOW_LEARNING_GUIDE.md (← Detailed guide)
└── DAG_QUICK_REFERENCE.md (← This file)
```

---

## ⚡ Quick Commands

```bash
# List all DAGs
docker-compose exec airflow-cli airflow dags list

# Trigger a DAG
docker-compose exec airflow-cli airflow dags trigger 01_beginner_hello_world

# Get DAG details
docker-compose exec airflow-cli airflow dags info 01_beginner_hello_world

# View all tasks in a DAG
docker-compose exec airflow-cli airflow tasks list 02_beginner_sequential_tasks

# Check Airflow status
docker-compose ps

# Restart services
docker-compose restart

# View logs
docker-compose logs -f scheduler
```

---

## ✅ Checklist for Learning

### Beginner Mastery
- [ ] Run `01_hello_world`
- [ ] Understand task dependencies in `02_sequential_tasks
`
- [ ] See parallelization in action with `03_parallel_tasks`
- [ ] Modify DAGs: Change schedule intervals, add print statements

### Intermediate Mastery
- [ ] Create different execution paths with `04_branching`
- [ ] Trigger failures intentionally in `05_error_handling`
- [ ] Use `06_multiple_operators` with your own commands
- [ ] Monitor a sensor in real-time with `07_sensors`
- [ ] Modify number of items in `08_dynamic_tasks`

### Advanced Mastery
- [ ] Build custom operator from scratch
- [ ] Create your first ETL DAG
- [ ] Organize a large DAG with TaskGroups
- [ ] Debug a failing task using logs
- [ ] Schedule a DAG to run at specific times

---

## 🎓 Next Level Resources

After mastering these 11 DAGs:

1. **Deploy to Production**
   - Set up Airflow on Kubernetes
   - Configure authentication
   - Set up monitoring

2. **Connect to Databases**
   - Use SqlOperator
   - Write to data warehouses
   - Query real databases

3. **Cloud Integration**
   - AWS (S3, Lambda, Glue)
   - GCP (BigQuery, Cloud Composer)
   - Azure (Blob Storage, Data Factory)

4. **Advanced Topics**
   - DAG Serialization
   - Trigger Rules
   - Task Pools
   - Priority Weights
   - Subdag vs TaskGroup

---

**Last Updated: 2026-02-24**
**Made with ❤️ for Airflow Learners**
"