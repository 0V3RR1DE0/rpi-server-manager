# RPI-SERVER-MANAGER

## Introduction
This is a simple web application for managing a Raspberry Pi server. Users can upload files to the server and view/download files shared by others.

## Features
- [x] View server generic info [disk space, cpu usage, others]
- [x] Upload files to the server.
- [x] View and download shared files.
- [x] Dynamic File Tabs
- [x] Responsive design for both desktop and mobile devices.

## Technologies Used
- HTML
- CSS
- JavaScript
- Flask (Python framework)
- Jinja2 (Template engine)

## Installation
1. Clone the repository:
    ```
    git clone https://github.com/0V3RR1DE0/rpi-server-manager.git
    ```

2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Run the application:
    ```
    python app.py
    ```

4. Open your web browser and navigate to `http://localhost:5000` to access the application.

5. Default login password is `123456`

## Usage
- Upon accessing the application, users can upload files using the provided form.
- Shared files are displayed on the main page, where users can click on them to download.
- Users can also view any uploaded files by clicking the "View Files" link.

## Planned Features
- [ ] Client Program
    - Allows you to manage multiple computers.
- [ ] Implement user authentication
- [ ] Better overall security
- [ ] Add file management capabilities (delete, move, rename)
- [ ] Improve server monitoring functionality
- [ ] Integrate with external storage services (Google Drive, Dropbox)
- [ ] Implement real-time file sharing notifications
- [ ] Enhance UI/UX design

## Features that need to be fixed
- [ ] Alerts/Notifications
- [ ] Network Logs
- [ ] Timeout to all html files
- [ ] No login bypass in web panel

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
