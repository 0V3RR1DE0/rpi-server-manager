# app.py

from flask import Flask, render_template, request, session, redirect, flash, url_for, send_from_directory, jsonify
from flask_bcrypt import Bcrypt
from datetime import timedelta
from functools import wraps
from tools.logger import log_access, log_file_upload
import os
from tools import system_monitor, network_logs as net_logs, logger
from flask_socketio import SocketIO, emit
import subprocess

# Initialize Flask app
app = Flask(__name__)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)

# Configuration
default_password = '123456'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the path for static files
app._static_folder = os.path.abspath("static")

# Try to read the secret key and hashed default password from the file
try:
    with open('secret_key.txt', 'r') as file:
        lines = file.readlines()

        # Check if the file contains both secret key and hashed password
        if len(lines) >= 2:
            secret_key = lines[0].strip()
            hashed_default_password = lines[1].strip()
        else:
            # If not, generate new ones
            raise FileNotFoundError

except FileNotFoundError:
    # If the file is not found or doesn't have enough lines, generate a new secret key and hashed default password
    import secrets
    secret_key = secrets.token_hex(16)
    hashed_default_password = bcrypt.generate_password_hash(default_password).decode('utf-8')

    # Save the new secret key and hashed default password to the file
    with open('secret_key.txt', 'w') as file:
        file.write(secret_key + '\n')
        file.write(hashed_default_password + '\n')

# Set Flask app configurations
app.secret_key = secret_key
app.permanent_session_lifetime = timedelta(minutes=5)

# Functions

def log_page_access():
    """Log access to a page."""
    ip_address = request.remote_addr
    action = f"Accessed {request.path}"
    log_access(ip_address, action)


def login_required(f):
    """Decorator to require login for certain routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please log in to access this page.', 'info')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes    
    
"""
##########################################################################
################################ ~BANNER~ ################################
##########################################################################
"""

@app.route('/get-logs')
def get_logs():
    logs = net_logs.get_network_logs()  # Corrected import
    return jsonify(logs)

@app.before_request
def before_request():
    """Redirect to login if not logged in."""
    if not session.get('logged_in'):
        if request.endpoint != 'static' and request.endpoint != 'login':
            return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route."""
    log_page_access()
    if request.method == 'POST':
        password_candidate = request.form['password']

        if bcrypt.check_password_hash(hashed_default_password, password_candidate):
            session.permanent = True
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect password. Try again.', 'error')

    return render_template('login.html')

@app.route('/change-password', methods=['POST'])
def change_password():
    """Change password route."""
    global hashed_default_password  # Declare as a global variable

    if not session.get('logged_in'):
        flash('Please log in to change the password.', 'info')
        return redirect(url_for('login'))

    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')

    if bcrypt.check_password_hash(hashed_default_password, current_password):
        # Update the hashed default password
        hashed_default_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        # Update the secret_key.txt file with the new hashed default password
        with open('secret_key.txt', 'w') as file:
            file.write(secret_key + '\n')
            file.write(hashed_default_password + '\n')

        flash('Password changed successfully!', 'success')
    else:
        flash('Incorrect current password. Try again.', 'error')

    return redirect(url_for('home'))


@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload file route."""
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('home'))

    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('home'))

    if file:
        # Log the file upload
        ip_address = request.remote_addr
        log_file_upload(ip_address, file.filename)
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flash('File uploaded successfully', 'success')
        return redirect(url_for('home'))

@app.route('/')
def home():
    """Home route."""
    log_page_access()
    if not session.get('logged_in'):
        flash('Please log in to access the home page.', 'info')
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/system-monitor')
@login_required
def system_monitor_route():
    """System monitor route."""
    log_page_access()
    return system_monitor.render_system_monitor()

@app.route('/network-tools')
@login_required
def network_tools():
    """Network tools route."""
    log_page_access()
    return render_template('network/network_tools.html')

@app.route('/network-tools/network-logs')
@login_required
def network_logs():
    """Network logs route."""
    log_page_access()
    # Retrieve and pass network logs data to the template
    logs = net_logs.get_network_logs()  # Corrected import
    return render_template('network/network_logs.html', logs=logs)

@app.route('/network-tools/network-statistics')
@login_required
def network_statistics():
    """Network statistics route."""
    log_page_access()
    return render_template('network/network_statistics.html')

@app.route('/file-share')
@login_required
def file_share():
    """File share route."""
    log_page_access()
    return render_template('file_sharing_service/file_share.html')

@app.route('/file-share/files')
@login_required
def file_share_files():
    """File share files route."""
    log_page_access()
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('file_sharing_service/files.html', files=files)

@app.route('/file-share/download/<filename>')
@login_required
def download_file(filename):
    """Download file route."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout')
def logout():
    """Logout route."""
    session.pop('logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/terminal', methods=['GET', 'POST'])
@login_required
def terminal():
    """Terminal route."""
    current_path = os.getcwd()
    log_page_access()
    return render_template('terminal.html', current_path=current_path)  # Pass the current path to the template

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    output = ""
    current_path = os.getcwd()  # Get the current path before executing the command
    try:
        if command.startswith("cd "):
            directory = command.split(" ", 1)[1]
            os.chdir(directory)
            output = os.getcwd()
        elif command == "cd..":  # Check if the command is 'cd..'
            os.chdir('..')  # Go back one directory
            output = os.getcwd()
        elif command == "cls" or command == "clear":  # Check if the command is 'cls' or 'clear'
            output = ""  # Clear the output area silently
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout.strip() if result.stdout else result.stderr.strip()
    except Exception as e:
        output = str(e)
    return jsonify({'output': output, 'current_path': current_path})  # Return both output and current path



# Run the app
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
