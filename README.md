# OOFPF
habit-tracker

## Project Overview:

This is a Python-based command-line habit tracking application that helps users establish and track daily/weekly habits. The project utilizes object-oriented programming (Habit class) and functional programming (analytics module), with SQLite for data persistence.

## ✨ Features

✅ Create daily or weekly habits

✅ Mark habits as complete, with automatic streak calculation

✅ View habit status and statistics

✅ Export data to JSON/CSV formats

✅ Upcoming habit reminders

✅ One-click demo data generation

✅ SQLite database storage

## 📦 Installation
### System Requirements
Python 3.7+

SQLite3

### Installation Steps
1. Clone the project or download the ``` habit_tracker.py ```file

2. Install dependencies:
```bash
pip install click
```

## 🚀 Quick Start
1. Initialize Database
```bash
python habit_tracker.py init
```

2. Create Your First Habit
```bash
# Create a daily habit
python habit_tracker.py create --name "Running" --periodicity daily --description "Run for 30 minutes every morning"

# Create a weekly habit
python habit_tracker.py create --name "Cleaning" --periodicity weekly --description "Clean the house every Sunday"
```

3. Mark Habit as Complete
```bash
ython habit_tracker.py complete --name "Running"
```

4. View All Habits
```bash
python habit_tracker.py list-habits
```

## 📖 Complete Command Guide
### Basic Commands
| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize database | `python habit_tracker.py init` |
| `create` | Create new habit | `python habit_tracker.py create --name "Reading" --periodicity daily` |
| `complete` | Mark habit as complete | `python habit_tracker.py complete --name "Reading"` |
| `list-habits` | List all habits | `python habit_tracker.py list-habits` |
| `stats` | View statistics | `python habit_tracker.py stats` |
| `delete` | Delete habit | `python habit_tracker.py delete --name "Reading"` |

### Advanced Features
| Command | Description | Example |
|---------|-------------|---------|
| `export` | Export data | `python habit_tracker.py export --format json --output my_habits.json` |
| `reminders` | View upcoming habits | `python habit_tracker.py reminders` |
| `demo` | Create demo data | `python habit_tracker.py demo` |
| `reset` | Reset all data | `python habit_tracker.py reset` |

## 🔧 Detailed Usage
### Creating Habits
```bash
python habit_tracker.py create \
  --name "habit_name" \
  --periodicity daily/weekly \
  --description "Optional description"
```

### Viewing Statistics
```bash
python habit_tracker.py stats
```
Example output:
```text
📊 Habit Stats
========================================
Total habits: 5
Daily habits: 3
Weekly habits: 2
Broken habits: 1

📈 Streak ranking:
  1. Running: 15 days
  2. Reading: 7 days
```

### Exporting Data
Supports JSON and CSV formats:
```bash
# Export as JSON
python habit_tracker.py export --format json --output habits.json

# Export as CSV
python habit_tracker.py export --format csv --output habits.csv
```

## 📊 Database Structure
### habits Table
| Field | Type | Description |
|---------|-------------|---------|
| id | INTEGER | Primary key |
| name | TEXT | Habit name |
| description | TEXT | Habit description |
| periodicity | TEXT | Periodicity (daily/weekly) |
| creation_date | TEXT | Creation time |
| current_streak | INTEGER | Current streak |
| longest_streak | INTEGER | Longest historical streak |

### completions Table
| Field | Type | Description |
|---------|-------------|---------|
| id | INTEGER | Primary key |
| habit_id | INTEGER | Foreign key |
| completion_time | TEXT | Completion time |

## 🎯 Concepts Explained
### Streak Calculation
Daily habits: Consecutive daily completion, resets if interrupted

Weekly habits: Consecutive weekly completion, resets if interrupted

Longest streak: Records historical best performance

### Habit Status
✅ Active: Completed before deadline

❌ Broken: Not completed by deadline

### Deadlines
Daily habits: End of day (midnight)

Weekly habits: End of week (Sunday 23:59:59)

### 🧪 Demo Mode
To quickly experience all features, use demo mode:
```bash
python habit_tracker.py demo
python habit_tracker.py list-habits
python habit_tracker.py stats
```

## 🔄 Data Migration
### Backup Data
```bash
python habit_tracker.py export --format json --output backup.json
```

### Restore Data
Currently requires manual import.

## 🐛 Troubleshooting
### Common Issues
#### 1. "Error: habit already exists"

Habit names must be unique

#### 2. "Error: habit not found"

Verify habit name spelling

Use ```list-habits``` to view all habits

#### 3. Inaccurate streak calculation

Ensure system time is correct

Don't skip dates when using ```complete``` command
