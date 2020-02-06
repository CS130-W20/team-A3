function sent_message(text) {
  return '<div class="row msg_container base_sent"><div class="col-md-8 col-xs-8 col-lg-8 col-sm-8"><div class="messages msg_sent"><p>'+text+'</p></div></div></div>';
}

function receive_message(text) {
  return '<div class="row msg_container base_receive"><div class="col-md-8 col-xs-8 col-lg-8 col-sm-8"><div class="messages msg_receive"><p>'+text+'</p></div></div></div>';
}

$("#chatbox_submit").click(function() {
    var data_text = $("#chatbox-input").val();
    var sent_div = sent_message(data_text);
    //var receive_div = receive_message('You said: ' + data_text);
    $('chat_log').append(sent_div);
    // let the chatbot in the backend handle it
    var data = {
      data: JSON.stringify({
        "text": data_text,
      })
    };
    $.ajax({
      url: "/chatbot_handle",
      type: "POST",
      data: data,
      dataType: 'json',
      success: function(data) {
        if (data[0].success == 1) {
          //console.log("succeed");
          var receive_div = receive_message(data[0].reply);
          $('chat_log').append(receive_div);
          clearInput();
          // scroll to the bottom
          $(".msg_container_base").stop().animate({ scrollTop: $(".msg_container_base")[0].scrollHeight}, 1000);
        } else {
          console.log("something wrong in the backend");
        }
      },
      error: function(xhr, type) {
        console.log("error", xhr, type);
      }
    });
});

function clearInput() {
    $("#chatbox-input").val('');
}

function collapse_chat(command='hide') {
    $('#chat_window_content').collapse(command)
}

function click_collapse(elem) {
    // console.log(elem.style.top);
    //console.log
    $('#chat_window_content').collapse('toggle');
}

$('#chatbox_draggable').draggable({containment: "window", axis: "x"});

$(window).resize(function() {
  // This will execute whenever the window is resized
  //$(window).height(); // New height
  //$(window).width(); // New width
  //console.log($('#chat_window_content').attr("aria-expanded"));
  var location = $(window).height() - 48;
  // console.log(location);
  $("#chatbox_draggable").css('top', location);
  collapse_chat('hide');
});

$(window).init(function() {
  var location = $(window).height() - 48;
  $("#chatbox_draggable").css('top', location);
  collapse_chat('hide');
});


// show.bs.collapse This event fires immediately when the show instance method is called.
// shown.bs.collapse   This event is fired when a collapse element has been made visible to the user (will wait for CSS transitions to complete).
// hide.bs.collapse    This event is fired immediately when the hide method has been called.
// hidden.bs.collapse
$('#chat_window_content').on('hide.bs.collapse', function () {
  // do something...
  // console.log("hidden");
  var location = $(window).height() - 48;
  $("#chatbox_draggable").css('top', location);
})

$('#chat_window_content').on('show.bs.collapse', function () {
  // do something...
  console.log("show");
  var location = $(window).height() * .5 - 108;
  // console.log(location);
  $("#chatbox_draggable").css('top', location);
})

$('#chat_window_content').on('hidden.bs.collapse', function () {
  document.getElementById("chat_icon").className = "fa fa-chevron-circle-right"
})

$('#chat_window_content').on('shown.bs.collapse', function () {
  // do something...
  document.getElementById("chat_icon").className = "fa fa-chevron-circle-down"
})
// $("div").animate({top: '80vh'});





