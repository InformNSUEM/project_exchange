function getCookie(name) {
    let cookieValue = null;
    console.log("12345")
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
                console.log("Sucess")
            } else {

                if (data['error']) {
                    $('#login-form__error').show().text(data['error']);
                }
            }
        }
    })
})
})