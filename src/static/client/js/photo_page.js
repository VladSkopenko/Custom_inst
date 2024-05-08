document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const imageId = urlParams.get('imageId');

    fetchImageDetails(imageId)
        .then(data => {
            const imageDetailsContainer = document.querySelector('.image-details-container');
            const template = getImageDetailsTemplate(data);
            imageDetailsContainer.innerHTML = template;

            // Fetch comments for the image and render them
            renderComments(data);
        })
        .catch(error => console.error('Error fetching image details:', error));
});

function fetchImageDetails(imageId) {
    const imageUrl = `/api/images/${imageId}`;
    return fetch(imageUrl)
        .then(response => response.json())
}
function getImageDetailsTemplate(data) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= data.rating) {
            stars += `<span class="fa fa-star checked"></span>`;
        } else {
            stars += `<span class="fa fa-star"></span>`;
        }
    } // This was missing

    return `
        <h1 class="text-primary">${data.image.title}</h1>
        <p><img id="photo" src="${data.image.base_url}" alt="Photo"></p>
        <div class="image-details text-primary">
            <p>User: ${data.image.user.nickname}</p>
            <p>Description: ${data.image.description}</p>
            <p>Created At: ${formatDate(data.image.created_at)}</p>
            <p>Updated At: ${formatDate(data.image.updated_at)}</p>
            <a href="rate_photo.html">
                <p id="rating" hidden>Rating: ${data.rating}</p>
                ${stars}
            </a>
            <div class="comments">
                <h3>Comments</h3>
                <ul id="commentsList"></ul>
                <a class="btn btn-sm btn-primary mt-4 p-1" href="/static/client/post_comment.html?imageId=${data.image.id}">POST Comment</a>
            </div>
        </div>
    `;
}



function formatDate(dateString) {
    const date = new Date(dateString);
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
}

function renderComments(comments_info) {
    console.log('comments_info: ', comments_info)
    const comments = comments_info.comments_info
    const commentsList = document.getElementById('commentsList');
    comments.forEach(comment => {
        const listItem = createCommentElement(comment);
        commentsList.appendChild(listItem);
    });
}

function createCommentElement(comment) {
    const listItem = document.createElement('li');
    listItem.innerHTML = `
        <a href="">
            <div class="comment">
                <p>${comment.comment}</p>
                <p>Posted at: ${formatDate(comment.created_at)}</p>
            </div>
        </a>
    `;
    return listItem;
}
