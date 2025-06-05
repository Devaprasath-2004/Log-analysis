# Import necessary modules
from flask import Flask, render_template
import sqlite3  # Used for connecting to the local logs.db SQLite database

# Initialize Flask application
app = Flask(__name__)

# Function to fetch logs from the database filtered by log_type (e.g., 'auth' or 'kern')
def fetch_logs_by_type(log_type):
    conn = sqlite3.connect('logs.db')  # Connect to the SQLite database
    c = conn.cursor()
    # Query logs where log_type matches the requested one
    c.execute("SELECT timestamp, user_name, log, defect FROM defective_logs WHERE log_type = ?", (log_type,))
    logs = c.fetchall()  # Fetch all matching records
    conn.close()
    return logs

# Route: Homepage
@app.route('/')
def home():
    # Render a homepage with links or info (home.html template required)
    return render_template('home.html')

# Route: Authentication logs
@app.route('/auth')
def auth_logs():
    logs = fetch_logs_by_type('auth')  # Fetch logs where log_type is 'auth'
    return render_template('dashboard.html', logs=logs, title='Auth Log Errors')

# Route: Kernel logs
@app.route('/kernel')
def kernel_logs():
    logs = fetch_logs_by_type('kern')  # Fetch logs where log_type is 'kern'
    return render_template('dashboard.html', logs=logs, title='Kernel Log Errors')

# Run the application on port 5050 and enable debug mode
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
