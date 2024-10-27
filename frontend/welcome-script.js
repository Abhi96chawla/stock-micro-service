document.addEventListener("DOMContentLoaded", function() {
    // Fetch user info on load
    fetch('/api/welcome')
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                // If not authorized, redirect to login page
                window.location.href = '/index';
            }
        })
        .then(data => {
            document.getElementById('welcome-message').textContent = data.message;  // Show welcome message
        });

    // Logout button event listener
    document.getElementById('logout-button').addEventListener('click', function() {
        fetch('/api/logout', {
            method: 'POST',
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/index';  // Redirect to login page after logout
            }
        });
    });
});
