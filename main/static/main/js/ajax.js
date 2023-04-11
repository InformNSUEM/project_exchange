function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

//Авторизация пользователя
$(document).ready(function() {
$('.login-form').on('submit', function (event){
    $('#register-form__error').text('')
    event.preventDefault();
    var form = $(this);
    
   
    const email = $('.login-form #username').val()
    const password = $('.login-form #password').val()
    
    const url = $(".login-form").attr("data-url");

    $.ajax({
        type: 'post',
        data: {
            "email": email,
            "password": password,
            "csrfmiddlewaretoken": getCookie('csrftoken'),
        },
 
        url: url,
        dataType: 'json',
        success: function (data){
            if (data['success']){
                console.log("Sucess");
                window.location.replace("/system/");
            } else {

                if (data['error']) {
                    $('#login-form__error').show().html(data['error']);
                }
            }
        }
    })
})
})





$(document).ready(function() {
$('.customer_request').on('submit', function (event){
  //$('#register-form__error').text('')
  event.preventDefault();
  var form = $(this);
  form.find('.is-invalid').removeClass('is-invalid');
  form.find('.invalid-feedback').remove();

  const url = $(".customer_request").attr("data-url");

  $.ajax({
      type: 'post',
      data: $(this).serialize(),
      url: url,
      dataType: 'json',
      success: function (data){
          if (data['success']){
              $('.customer_request').hide()
              $('.register-success').show()
          } else {
              for (var fieldName in data.errors) {
                  var field = $('#id_' + fieldName);
                  field.addClass('is-invalid');
                  field.after('<div class="invalid-feedback">' + data.errors[fieldName] + '</div>');
              }
              if (data['error']) {
                  $('#register-form__error').show().text(data['error']);
              }
          }
      }
  })
})
})