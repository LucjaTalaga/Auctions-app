document.addEventListener("DOMContentLoaded", function() {
    const defImg = 'https://upload.wikimedia.org/wikipedia/commons/2/2a/3D_illustration_image_of_a_gavel_-_auction_hammer_-_free_to_use_in_your_projects_08.jpg';
    const images = document.querySelectorAll('img');

    for (let i =0; i<images.length; i++){
        images[i].addEventListener("error", function () {
            this.setAttribute("src", defImg);
        })
    }
})