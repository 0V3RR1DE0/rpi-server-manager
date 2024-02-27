from flask import Flask, render_template, request, session, redirect, flash, url_for, send_from_directory
from flask_bcrypt import Bcrypt
from datetime import timedelta
from tools import system_monitor
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Default password
default_password = '123456'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/login', methods=['GET', 'POST'])
def login():
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
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))

    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flash('File uploaded successfully', 'success')
        return redirect(url_for('index'))

@app.route('/')
def home():
    if not session.get('logged_in'):
        flash('Please log in to access the home page.', 'info')
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/system-monitor')
def system_monitor_route():
    return system_monitor.render_system_monitor()

@app.route('/network-tools')
def network_tools():
    return render_template('network/network_tools.html')

@app.route('/network-logs')
def network_logs():
    return render_template('network/network_logs.html', network_logs=network_logs.get_network_logs())

@app.route('/network-statistics')
def network_statistics():
    return render_template('network/network_statistics.html')

@app.route('/file-share')
def file_share():
    return render_template('file_sharing_service/file_share.html')

@app.route('/file-share/files')
def file_share_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('file_sharing_service/files.html', files=files)

@app.route('/file-share/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
