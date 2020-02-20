// Print to log
function print(something) {
    console.log(something);
}

// Redirects click on icon to button which triggers modal
$("#avatar-icon").click(function() {
    $("#change-avatar").click();
});

// Set new description with POST on click on 'Update'
$('#update-description').click(function() {
    $.post(
      URL='/home/update_description',
      data={'new_desc': $('textarea.form-control').val()},
      function(data) {
        //do nothing
      }
    );
    return false;
  });
