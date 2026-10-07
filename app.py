import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def init_db():
    """Initializes the SQLite database and creates the tasks table."""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    # SQL query to build the database table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Fetches all tasks from the database and displays them on the website."""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    # SQL query to fetch all tasks
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Handles the form submission to insert a new task into the database."""
    task_title = request.form.get('title')
    if task_title:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        # SQL query to insert safe parameter data into the table
        cursor.execute('INSERT INTO tasks (title) VALUES (?)', (task_title,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Deletes a task based on its unique ID."""
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    # SQL query to remove data from the table
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # Run the database setup script
    app.run(debug=True)
