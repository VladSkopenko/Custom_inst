// Ensure LOGOUT_URL is defined properly
const LOGOUT_URL = `${BASE_URL}/api/auth/logout`;

// Function to handle logout
const logout = () => {
    // Send POST request to logout endpoint
    fetch(LOGOUT_URL)
        .then(response => response.json())
        .then(data => {
            // Clear access token, refresh token, and username from local storage
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('username');
            // Set user as logged out
            localStorage.setItem('logged', 'false');
            // Redirect to index.html
            window.location.href = "/";
        })
        .catch(error => console.error('Error logging out:', error));
};

document.addEventListener("DOMContentLoaded", function () {
    // Attach logout function to logout button click event
    document.getElementById("logout-btn").addEventListener("click", logout);
});
