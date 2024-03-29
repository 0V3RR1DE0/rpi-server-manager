# RPI-SERVER-MANAGER

## Introduction
Server management web application that allows file share, web terminal, other stuff.

## Features
- [x] View server generic info [disk space, cpu usage, others]
- [x] Upload files to the server.
- [x] View and download shared files.
- [x] Dynamic File Tabs
- [x] Responsive design for both desktop and mobile devices.
- [x] Terminal

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

## File Structure
```
rpi-server-manager/
│
├── app.py
├── static/
│        ├── data/
│        │      ├── logs/
│        │      └──    └── log_{datetime}.log
│        ├── js/
│        │    ├── tools/
│        │    │       └── network_logs.js
│        │    └── alerts.js
│        └── styles.css
│
├── templates/
│           ├── file_sharing_service/
│           │                      ├──  file_share.html
│           │                      └──  files.html
│           │
│           ├── network/
│           │         ├──  network_logs.html
│           │         ├──  network_statistics.html
│           │         └──  network_tools.html
│           │
│           ├── index.html
│           ├── login.html
│           ├── system_monitor.html
│           └── terminal.html
│
├── tools/
│       ├── network_logs.py
│       ├── logger.py
│       └── system_monitor.py
└── uploads/
```

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
- [ ] Terminal multi line output

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
