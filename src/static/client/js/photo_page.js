
document.addEventListener("DOMContentLoaded", function () {
    // Extract parameters from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const imageId = urlParams.get('imageId');
    const tagsId = urlParams.get('tagsId');
    const commentsInfo = urlParams.get('commentsInfo');
    const rating = urlParams.get('rating');

    // Fetch image details using the provided parameters (you may replace this with your own API call)
    fetchImageDetails(imageId)
        .then(data => {
            // Create HTML elements for image details
            const imageTitleElement = document.createElement('h2');
            imageTitleElement.textContent = data.image.title;

            const imageElement = document.createElement('img');
            imageElement.id = 'photo';
            imageElement.src = data.image.base_url;
            imageElement.alt = 'Photo';

            const userNicknameElement = document.createElement('p');
            userNicknameElement.textContent = `User: ${data.image.user.nickname}`;

            const descriptionElement = document.createElement('p');
            descriptionElement.textContent = `Description: ${data.image.description}`;

            const createdAtElement = document.createElement('p');
            createdAtElement.textContent = `Created At: ${data.image.created_at}`;

            const updatedAtElement = document.createElement('p');
            updatedAtElement.textContent = `Updated At: ${data.image.updated_at}`;

            const ratingElement = document.createElement('p');
            ratingElement.textContent = `Rating: ${data.rating}`;

            // Append created elements to the container
            const imageDetailsContainer = document.querySelector('.image-details-container');
            imageDetailsContainer.appendChild(imageTitleElement);
            imageDetailsContainer.appendChild(imageElement);
            imageDetailsContainer.appendChild(userNicknameElement);
            imageDetailsContainer.appendChild(descriptionElement);
            imageDetailsContainer.appendChild(createdAtElement);
            imageDetailsContainer.appendChild(updatedAtElement);
            imageDetailsContainer.appendChild(ratingElement);

            // Create button for POST requests
            const postCommentButton = document.createElement('button');
            postCommentButton.id = 'postCommentButton';
            postCommentButton.textContent = 'POST Comment';

            // Add button click event listener for POST requests
            postCommentButton.addEventListener('click', function () {
                // Make POST request to create a comment
                fetch(`/api/comments/create/${comment_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        // Include comment data here
                    })
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Failed to create comment');
                        }
                        // Handle successful response
                    })
                    .catch(error => console.error('Error creating comment:', error));
            });

            // Append button to the container
            imageDetailsContainer.appendChild(postCommentButton);
        })
        .catch(error => console.error('Error fetching image details:', error));
});

function fetchImageDetails(imageId) {
    const imageUrl = `/api/images/${imageId}`; 
    return fetch(imageUrl)
        .then(response => response.json());
}

