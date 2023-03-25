
function showImage(img){
    var selectedImage = document.getElementById('selected-image');
    selectedImage.src = img.src;


    var selectedImage1 = document.getElementById('temp');
    selectedImage1.value = img.src;
}
