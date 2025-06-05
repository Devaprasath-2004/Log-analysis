This project is a lightweight log monitoring tool that:
•	Parses system log files like /var/log/auth.log and /var/log/kern.log.
•	Detects and extracts defective log entries (e.g., errors, failures, denied access).
•	Stores the defective entries in a local SQLite database.
•	Displays logs via a simple Flask web dashboard.
Perfect for system admins or developers looking for a minimal, portable, and visual log tracking tool.
________________________________________
Project Structure
project/
├── log_parser.py            # Parses logs and stores defects in logs.db
├── app.py                   # Flask web app to display logs
├── logs.db                  # SQLite database (auto-created)
└── templates/
    ├── home.html            # Homepage with navigation links
    └── dashboard.html       # Displays defective logs in a styled table
________________________________________
Setup Instructions
1. Requirements
•	Python 3.x
•	Flask
Install Flask if you haven't:
pip install flask
________________________________________
2. Step-by-Step Usage
Step 1: Parse the Logs
Run the following script to extract and store defective logs:
python log_parser.py
This reads from:
•	/var/log/auth.log
•	/var/log/kern.log
And stores error-related lines into logs.db.
Note: You might need sudo permissions to access these log files.
Step 2: Launch the Web Dashboard
python app.py
Visit http://localhost:5050 in your browser.
________________________________________
Web Interface Routes
Route	Description
/	Home page
/auth	View defective authentication logs
/kernel	View defective kernel logs
________________________________________
How It Works
1. log_parser.py
•	Scans logs for keywords: error, fail, denied, segfault, invalid, panic
•	Extracts timestamp and device hostname
•	Classifies logs into:
o	auth error if from auth.log
o	kernel error if from kern.log
•	Saves them in SQLite (logs.db) using the schema:

CREATE TABLE defective_logs (
    	id INTEGER PRIMARY KEY AUTOINCREMENT,
    	timestamp TEXT,
    	user_name TEXT,
    	log TEXT,
    	defect TEXT,
    	log_type TEXT
       )
________________________________________
2. app.py (Flask Server)
•	Fetches logs by type (auth, kern) from the database.
•	Renders logs using HTML templates:
o	home.html – links to view different log types.
o	dashboard.html – dynamic table displaying log entries.
________________________________________
3. dashboard.html
•	Displays a clean HTML table with:
o	Timestamp
o	User name (hostname)
o	Raw log message
o	Defect type
________________________________________
Notes
•	This is a lightweight solution and does not require heavy frameworks or external databases.
•	Ideal for local log analysis or as a base for future log monitoring tools.
•	Extendable to include filters, search, export to CSV, or integrate with a charting library like Chart.js.
________________________________________
Resetting the Database
To clear all logs and restart:
rm logs.db
python log_parser.py
