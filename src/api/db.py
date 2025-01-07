import sqlite3
from datetime import datetime
from api.task import Task

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('tasks.db')
c = conn.cursor()

# Create tasks table
c.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATETIME,
    priority TEXT,
    tags TEXT,
    completed INTEGER,
    created_at TEXT,
    recurrence TEXT
)
''')
conn.commit()
# Create task_logs table
c.execute('''
CREATE TABLE IF NOT EXISTS task_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    status TEXT,
    log_time TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(task_id) REFERENCES tasks(id)
)
''')

conn.commit()
conn.close()

def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to save a task to the database
def save_task(task):
    conn = get_db_connection()
    c = conn.cursor()
    with conn:
        c.execute('''
        INSERT INTO tasks (title, description, due_date, priority, tags, completed, created_at, recurrence)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (task.title, task.description, task.due_date, task.priority, ','.join(task.tags), int(task.completed), task.created_at, task.recurrence))
    conn.commit()
    conn.close() 

# Function to retrieve all tasks from the database
def get_tasks():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return [Task(*task) for task in tasks]

# Function to retrieve a task by ID from the database

def get_task_by_id(task_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    conn.close()
    if task:
        return Task(*task)
    return None

# Function to update a task in the database
def update_task(task_id, task):
    conn = get_db_connection()
    c = conn.cursor()
    with conn:
        c.execute('''
        UPDATE tasks
        SET title = ?, description = ?, due_date = ?, priority = ?, tags = ?, completed = ?, created_at = ?, recurrence = ?
        WHERE id = ?
        ''', (task.title, task.description, task.due_date, task.priority, ','.join(task.tags), int(task.completed), task.created_at, task.recurrence, task_id))
        conn.commit()
        conn.close()
# Function to delete a task from the database
def delete_task(task_id):
    conn = get_db_connection()
    c = conn.cursor()
    with conn:
        c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        # Function to retrieve tasks for a specific day
def get_tasks_for_day(date):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
    SELECT * FROM tasks
    WHERE (DATE(due_date) = ? AND recurrence = 'once') OR (DATE(due_date) >= ? AND recurrence = 'daily')
    ''', (date,date))
    tasks = c.fetchall()
    print(tasks)
    conn.close()
    return [Task(*task) for task in tasks]
# Example usage
if __name__ == "__main__":
    get_tasks_for_day("2025-01-08")
    print("Task saved to database.")