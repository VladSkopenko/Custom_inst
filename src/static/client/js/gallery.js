
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
            id,
            user_id,
            title,
            base_url,
            transform_url,
            description,
            qr_url,
            created_at,
            updated_at,
            user
        } = photo;
        let photoTitle = title;
        let maxCharactersPerPhotoTitle = 30;
        photoTitle =
            photoTitle.length > maxCharactersPerPhotoTitle
                ? photoTitle.slice(0, maxCharactersPerPhotoTitle) + '...'
                : photoTitle;
        const createdDate = new Date(created_at);
        const formattedCreatedDate = `${createdDate.getDate().toString().padStart(2, '0')}-${(createdDate.getMonth() + 1).toString().padStart(2, '0')}-${createdDate.getFullYear()}`;
        const updatedDate = new Date(updated_at);
        const formattedUpdatedDate = `${updatedDate.getDate().toString().padStart(2, '0')}-${(updatedDate.getMonth() + 1).toString().padStart(2, '0')}-${updatedDate.getFullYear()}`;
        return `<li class="photo" data-id=${id}>
  <div class = "photo-image__wrapper">
  <img src="${base_url}" alt="${title}" data-updated_at=${formattedUpdatedDate} data-qr_url=${qr_url} data-transform_url=${transform_url}/>
  </div>
  <p class="photo__title">${photoTitle}</p>
  <p class="photo__user" user-id=${user_id} data-user=${user}>${user.nickname}</p>
  <div class="photo__position">
   <p class="photo__description">${description}</p>
  <p class="photo__description">|</p>
  <p class="photo__year">${formattedCreatedDate}</p>
  </div>
 
  </li>
  `;

    }).join('');
    document.querySelector('#js-list').innerHTML = markup;

}



