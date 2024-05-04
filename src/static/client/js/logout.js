const LOGOUT_URL = `${BASE_URL}/api/auth/logout`;

// Function to handle logout
const logout = () => {
    const currentUrl = window.location.href;
    console.log(currentUrl);

    console.log('Logout_url: ', LOGOUT_URL)
    const accessToken = localStorage.getItem('access_token');
    fetch(LOGOUT_URL, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${accessToken}`, // Include the access token in the Authorization header
            'Content-Type': 'application/json' // Specify the content type
        },
        body: JSON.stringify({}) // Empty body for the POST request
    })
        .then(response => console.log(response.json()))
        .then(data => {
            // Clear access token, refresh token, and username from local storage
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('username');
            // Set user as logged out
            localStorage.setItem('logged', 'false');
            // Redirect to index.html
            window.location.href = "/";
            // Log success message to console
            console.log('Logged out successfully');
            
        })
        .catch(error => console.error('Error logging out:', error));
};

    document.addEventListener("DOMContentLoaded", function () {
    // Attach logout function to logout button click event
    document.getElementById("logout-btn").addEventListener("click", logout);
});
