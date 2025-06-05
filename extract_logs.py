# Import required modules
import sqlite3          # For interacting with the SQLite database
import re               # For parsing log lines using regular expressions
import socket           # For retrieving the device (hostname)
from datetime import datetime  # (Optional in case needed for date/time operations)

# Step 1: Connect to SQLite database (creates 'logs.db' if it doesn't exist)
conn = sqlite3.connect('logs.db')
c = conn.cursor()

# Step 2: Create a table to store defective logs if it doesn't already exist
# The table includes: id, timestamp, user_name, raw log content, defect type, and log type
c.execute('''
CREATE TABLE IF NOT EXISTS defective_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    user_name TEXT,
    log TEXT,
    defect TEXT,
    log_type TEXT
)
''')

# Step 3: Function to parse a given log file and store defective log entries into the database
def parse_log(file_path, source):
    # Get the device hostname to use as a user identifier
    device_name = socket.gethostname()
    
    # Open the log file for reading
    with open(file_path, 'r') as f:
        for line in f:
            # Check if the line contains error-related keywords
            if any(err in line.lower() for err in ['error', 'fail', 'denied', 'segfault', 'invalid', 'panic']):
                # Extract the timestamp using regex (e.g., "Jan 1 00:00:00")
                timestamp_match = re.match(r'^(\w+\s+\d+\s[\d:]+)', line)
                timestamp = timestamp_match.group(1) if timestamp_match else 'Unknown'

                # Use hostname as the user name
                user = device_name

                # Determine defect type and log type based on the file source
                defect_type = "auth error" if "auth" in source else "kernel error"
                log_type = 'auth' if "auth" in source else 'kern'

                # Insert the parsed data into the defective_logs table
                c.execute('''INSERT INTO defective_logs (timestamp, user_name, log, defect, log_type)
                             VALUES (?, ?, ?, ?, ?)''',
                          (timestamp, user, line.strip(), defect_type, log_type))

    # Commit the transaction after parsing is done
    conn.commit()

# Step 4: Call the function to parse both kernel and auth log files
parse_log('/var/log/kern.log', 'kernel')   # Parse kernel logs
parse_log('/var/log/auth.log', 'auth')     # Parse authentication logs

# Step 5: Close the database connection
conn.close()
