const ALL_IMG_URL = `${BASE_URL}/api/images/all`;

document.addEventListener("DOMContentLoaded", function () {
    // Fetch data from the API endpoint
    fetch(ALL_IMG_URL)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            // Reference to the <ul> element
            const galleryList = document.getElementById('js-list');

            // Iterate over the array of images
            data.forEach(image => {
                // Create list item for each image
                const listItem = document.createElement('li');
                listItem.classList.add('card');

                // Create image element
                const imageElement = document.createElement('img');
                imageElement.src = image.base_url;
                imageElement.alt = image.title;

                // Append image element to list item
                listItem.appendChild(imageElement);

                // Create title element
                const titleElement = document.createElement('h2');
                titleElement.textContent = image.title;

                // Append title element to list item
                listItem.appendChild(titleElement);

                // Create description element
                const descriptionElement = document.createElement('p');
                descriptionElement.textContent = image.description;

                // Append description element to list item
                listItem.appendChild(descriptionElement);

                // Append list item to the <ul> element
                galleryList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error fetching images:', error));
});
