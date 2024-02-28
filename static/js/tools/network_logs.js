function fetchLogs() {
    fetch('/get-logs')
        .then(response => response.json())
        .then(data => {
            const logsList = document.getElementById('logs-list');
            logsList.innerHTML = ''; // Clear existing logs
            // Reverse the array to display the most recent logs first
            data.slice(-20).reverse().forEach(log => {
                const listItem = document.createElement('li');
                listItem.textContent = log;
                logsList.appendChild(listItem); // Add log to the list
            });
        })
        .catch(error => console.error('Error fetching logs:', error));
}

// Fetch logs initially and every 5 seconds thereafter
fetchLogs();
setInterval(fetchLogs, 5000);
