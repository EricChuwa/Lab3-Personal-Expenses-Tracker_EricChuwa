# Lab3-Personal-Expenses-Tracker_EricChuwa\n By Eric Chuwa

## Personal Expenses Tracker & Archiving Tool

### Overview
This project is a Python-based command-line personal expenses tracker designed for efficient financial management. It includes an archiving shell script (`archive_expenses.sh`) to manage, backup, and search expense history files.

### Features
- Track expenses, revenue, and balance with daily logs.
- Menu-driven CLI with options to view, add, and search transactions.
- Expenses and balance saved in plain text files for easy inspection.
- Archiving script organizes old expense logs, supports date-based search, and maintains an archive log.
- Modular design using Python classes for maintainability.

### Getting Started

#### Prerequisites
- Python 3.x (recommended)
- Bash shell (for archive_expenses.sh)
- Ubuntu or compatible Linux environment

#### Installation
Clone the repository:
```bash
git clone https://github.com/yourusername/expenses-tracker.git
cd expenses-tracker
```

#### Usage
Run the tracker:
```bash
python expenses_tracker.py
```
Archive expense files:
```bash
bash archive_expenses.sh
```
Search archive for a specific date:
```bash
bash archive_expenses.sh YYYY-MM-DD
```

### File Structure
- `expenses_tracker.py`: Main Python script with class-based financial tracker
- `archive_expenses.sh`: Bash script for file archiving and searching
- `balance.txt`: Stores current or historical balances
- `expensesYYYY-MM-DD.txt`: Daily transaction logs
- `archives/`: Folder for archived expense files

