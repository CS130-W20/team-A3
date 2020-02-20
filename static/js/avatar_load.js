function input_avatar_available(input) {
    return input.files && input.files[0];
}

function print(something) {
    console.log(something);
}

function readURL(input) {
    if (input_avatar_available(input)) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#imagePreview').css('background-image', 'url('+e.target.result +')');
            $('#imagePreview').hide();
            $('#imagePreview').fadeIn(650);
        }
        reader.readAsDataURL(input.files[0]);
    }
}
$("#imageUpload").change(function() {
    readURL(this);
});

$("#avatar-icon").click(function() {
    $("#change-avatar").click();
});

function image_submit() {
    $("#submitphotoModal").modal("hide");
    var imageUploaded = document.getElementById("imageUpload");

    var form = document.getElementById("imageInput");

    if (input_avatar_available(imageUploaded)) {
        // alert("Planning to use Ajax to update the image from here in the future;")
        form.submit();
    } else {
        alert("There isn't any update of your photo");
    }
};
