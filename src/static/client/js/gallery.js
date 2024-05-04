
const ALL_IMG_URL = `${BASE_URL}/api/images/all`;

document.addEventListener("DOMContentLoaded", function () {
    // Fetch data from the API endpoint
    fetch(ALL_IMG_URL)
        .then(response => response.json())
        .then(data => render_gallery(data)) // Pass the response data to render_gallery
        .catch(error => console.error('Error fetching images:', error));
});

const imageSize = 'w500';
function render_gallery(photos_data) {

    if (photos_data.length === 0) {
        document.querySelector('#js-list').innerHTML =
            '<p class="error_localstoragy">Nothing here...🤷🏽‍♀️</p>';
        return;
    }
    const markup = photos_data.map(photo => {
        const {
            image,
            tags_id,
            comments_info,
        } = photo;
        let photoTitle = image.title;
        let maxCharactersPerPhotoTitle = 30;
        photoTitle =
            photoTitle.length > maxCharactersPerPhotoTitle
                ? photoTitle.slice(0, maxCharactersPerPhotoTitle) + '...'
                : photoTitle;
        const createdDate = new Date(image.created_at);
        const formattedCreatedDate = `${createdDate.getDate().toString().padStart(2, '0')}-${(createdDate.getMonth() + 1).toString().padStart(2, '0')}-${createdDate.getFullYear()}`;
        const updatedDate = new Date(image.updated_at);
        const formattedUpdatedDate = `${updatedDate.getDate().toString().padStart(2, '0')}-${(updatedDate.getMonth() + 1).toString().padStart(2, '0')}-${updatedDate.getFullYear()}`;
        return `<li class="photo" data-id=${image.id}>
  <div class = "photo-image__wrapper">
  <img src="${image.base_url}" alt="${image.title}" data-updated_at=${formattedUpdatedDate} data-qr_url=${image.qr_url} data-transform_url=${image.transform_url}/>
  </div>
  <p class="photo__title">${photoTitle}</p>
  <p class="photo__user" user-id=${image.user_id} data-user=${image.user}>${image.user.nickname}</p>
  <div class="photo__position">
   <p class="photo__description">${image.description}</p>
  <p class="photo__description">|</p>
  <p class="photo__year">${formattedCreatedDate}</p>
  </div>
 
  </li>
  `;

    }).join('');
    document.querySelector('#js-list').innerHTML = markup;

}



