// https://github.com/PatriciaXiao/AutoQuiz_v2/blob/master/templates/welcome.html
//SERVING THE RIGHT FILE!
$(function () {
  //$(".alert").hide();
  $("#alert_of_login").hide();
  $('select').selectpicker();
  //console.log(browse_categories_json); // it is ready
  if (browse_categories_json != {}){
    var browse_sidebar = generate_leftsiderbar(browse_categories_json);
    //console.log(browse_sidebar);
  }
});

// https://stackoverflow.com/questions/41566247/bootstrap-resizing-the-page-not-finding-viewport
(function($, viewport){
  $(document).ready(function() {
    // Execute code each time window size changes
    $(window).resize(
      viewport.changed(function() {
        if(viewport.is('xs')) {
          change_maindiv_size("shrink");
        }
      })
    );
  });
})(jQuery, ResponsiveBootstrapToolkit);

function jsonCopy(src) {
  return JSON.parse(JSON.stringify(src));
}

function category_selected(item) {
  var item_id = item.getAttribute("id");
  //console.log(item);
  if (item_id == -1) {
    // nothing is selected
    console.log("nothing is selected");
  } else {
    console.log(item_id + " is selected");
  }
  var data = {
    data: JSON.stringify({
      "category_id": item_id,
    })
  };
  $.ajax({
      url: "/select_category",
      type: "POST",
      data: data,
      dataType: 'json',
      success: function(data) {
        if (data[0].success == 1) {
          console.log("succeed");
        } else {
          console.log("something wrong in the backend");
        }
      },
      error: function(xhr, type) {
        console.log("error", xhr, type);
      }
  });
}

function category_unselected(item) {
  var item_id = item.getAttribute("id");
  console.log(item_id + " is unselected");
}

//function sidebar_sub(json_data, parent, indent_level) {
function sidebar_sub(json_data_raw, parent, indent_level) {
  var json_data = jsonCopy(json_data_raw);
  //console.log(json_data);
  for (var idx = 0; idx < json_data.length; idx++) {
    //console.log(idx);
    var node_name = json_data[idx]["category_name"];
    var node_children = json_data[idx]["sub_categories"];
    var elem_id = json_data[idx]["id"];
    var node_id = "collapse_" + elem_id;
    var button = document.createElement('button');
    button.className = "btn btn-link my-btn-link ml-" + indent_level;
    button.innerHTML = node_name;
    button.id = elem_id;
    button.setAttribute("role", "button");
    button.setAttribute("type", "button");
    button.onclick = function(){category_selected(this);}
    button.onblur = function(){category_unselected(this);}
    if (node_children.length > 0) {
      button.innerHTML += '&nbsp;&nbsp;<i class="fa fa-list"></i>';
      button.setAttribute("data-toggle", "collapse");
      button.setAttribute("data-target", "#" + node_id);
      var children_div = document.createElement('div');
      children_div.className = "collapse";
      children_div.id = node_id;
      sidebar_sub(node_children, children_div, indent_level + 1);
    } else {
      button.className = button.className + " end_link";
    }
    // if(idx>0)
    //   parent.appendChild(document.createElement('hr'));
    parent.appendChild(button);
    if (node_children.length > 0) {
      parent.appendChild(children_div);
    } 
  }
}

function generate_leftsiderbar(json_data) {
  var root_id = "accordion_left";
  var target_div = document.getElementById(root_id);
  for (var idx = 0; idx < json_data.length; idx ++) {
    var id = json_data[idx]["id"];
    var category_name = json_data[idx]["category_name"];
    var sub_categories = json_data[idx]["sub_categories"];
    var header_id = "header_" + id;
    var body_id = "collapse_" + id;
    var obj = document.createElement('div');
    var body_obj = null;
    obj.className = 'card border border-white';
    obj.id = 'card_' + id;
    var header_obj = document.createElement('div');
    header_obj.className = "card-header";
    header_obj.id = header_id;
    var header_content = document.createElement('h2');
    header_content.className = "mb-0";
    var header_clickable = document.createElement('button');
    header_clickable.className = "btn btn-link my-btn-link-2";
    header_clickable.id = id;
    header_clickable.innerHTML = category_name;
    header_clickable.setAttribute("type", "button");
    header_clickable.setAttribute("data-toggle", "collapse");
    header_clickable.setAttribute("aria-expanded", "false");
    header_clickable.onclick = function(){category_selected(this);}
    header_clickable.onblur = function(){category_unselected(this);}
    if (sub_categories.length > 0) {
      // <i class="fa fa-list"></i>
      header_clickable.innerHTML += '&nbsp;&nbsp;<i class="fa fa-list"></i>';
      header_clickable.setAttribute("data-target", "#" + body_id);
      header_clickable.setAttribute("aria-controls", body_id);
      body_obj = document.createElement('div');
      body_obj.className = "collapse";
      body_obj.id = body_id;
      body_obj.setAttribute("aria-labelledby", header_id);
      body_obj.setAttribute("data-parent", "#" + root_id);
      //sidebar_sub(sub_categories, body_obj, 0);
      var body_div = document.createElement('div');
      body_div.className = "card-body border border-white";
      sidebar_sub(sub_categories, body_div, 1);
      body_obj.appendChild(body_div);
      //console.log("hello world");
      //console.log(body_obj);
    } else {
      header_clickable.className = header_clickable.className + " end_link";
    }
    header_content.appendChild(header_clickable);
    header_obj.appendChild(header_content);
    obj.appendChild(header_obj);
    if (body_obj)
      obj.appendChild(body_obj);
    target_div.appendChild(obj);
  }
  return target_div;
}

function show_password() {
  var x = document.getElementById("password");
  var x_conf = document.getElementById("password_confirm");
  if (x.type === "password") {
    x.type = "text";
    x_conf.type = "text";
  } else {
    x.type = "password";
    x_conf.type = "password";
  }
}

function show_confirm() {
  var x = document.getElementById("pwd_confirm");
  //console.log(x)
  //console.log(x.style.display)
  if (x.style.display === "none") {
    x.style.display = "";
  } else {
    x.style.display = "none";
  }
}

function check_valid_string(string_content) {
  // return string_content.matches("^[a-zA-Z0-9]+$");
  return string_content.match("^[a-zA-Z0-9\\ _@.]+$")
}

function check_valid_pwd(pwd) {
  return pwd.match("^[a-zA-Z0-9\\.;,:'@^!~#$%^&*-+_=]{1,32}$")
}

function check_valid_before_submit() {
  var form = document.getElementById("login_form");
  var reg = form.reg.checked;
  var username = $.trim(form.username.value); // form.username.value;
  var password = $.trim(form.password.value); // form.password.value;
  var confirm = $.trim(form.confirm.value); // form.confirm.value;
  form.username.value = username;
  form.password.value = password;
  form.confirm.value = confirm;
  var message = document.getElementById("login_format_message");
  //console.log(message)
  // var ready_submit = false;
  if (!check_valid_string(username)) {
    message.innerHTML = "We would recommend using your name, but nickname, id, or email address are also acceptable, as long as they contain ONLY characters (a-z, A-Z), blanks(in the middle of the string), numbers (0-9), underscore ('_'), dot ('.'), or at ('@').";
  } else if (username.length > 60) {
    message.innerHTML = "Your user name is way too long, could you please use a name that is not longer than 60 characters in total? Thank you for your understanding.";
  } else if (username.length == 0 || password.length == 0) {
    message.innerHTML = "Please check it again before submission, neither user name nor password should be blank.";
  } else if (!check_valid_pwd(password)) {
    message.innerHTML = "Password has to be a string contains ONLY characters (a-z, A-Z), numbers, or some of the special characters namely in this set (brackets excluded): ( . , : ; ! @ # $ % ^ & * + - = _ ~ ). And we also have a maximum length limit of 32. We do appreciate that you attempted to design a special password, and thank your for your understanding.";
  } else if (reg && password != confirm) {
    message.innerHTML = "please make sure that the password you entered matches the password confirmation before you submit this form";
  } else if (reg) {
    var data = {
      data: JSON.stringify({
        "username": username,
      })
    };
    $.ajax({
        url: "/usernamecheck",
        type: "POST",
        data: data,
        dataType: 'json',
        success: function(data) {
          console.log(data);
          if (data[0].success == 1) {
            //console.log("SUCCESS!");
            form.submit();
          } else {
            // user already exists
            message.innerHTML = "Sorry for the inconvenience, but user <b>" + username + "</b> already exists.";
            $('#alert_of_login').show();
          }
        },
        error: function(xhr, type) {
          console.log("error", xhr, type);
        }
    });
  } else {
    form.submit();
  }
  if (message.innerHTML.length > 0) {
    $('#alert_of_login').show();
  }
}

function change_maindiv_size(mode="switch") {
  var main_div = document.getElementById("main_div");
  var wide_style="col-xs-12 col-sm-12 col-lg-12 overflow-auto fixed_height";
  var narrow_style="col-xs-12 col-sm-9 col-lg-10 overflow-auto fixed_height";
  var left_navbar = document.getElementById("left_navbar");
  var hide_style = "col-xs-12 col-sm-3 col-lg-2 overflow-auto fixed_height collapse";
  var show_style = "col-xs-12 col-sm-3 col-lg-2 overflow-auto fixed_height"; // show
  if(main_div==undefined)
    return;
  if(mode=="shrink" || (mode=="switch" && left_navbar.className == show_style)) {
    left_navbar.className = hide_style;
    main_div.className = wide_style;
    return;
  } else if (mode=="expand" || (mode=="switch" && left_navbar.className == hide_style)) {
    left_navbar.className = show_style;
    main_div.className = narrow_style;
  }
}





