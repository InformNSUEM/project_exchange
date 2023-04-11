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

$(document).ready(function() {
$('.register-form-student').on('submit', function (event){
    $('#register-form__error').text('')
    event.preventDefault();
    var form = $(this);
    form.find('.is-invalid').removeClass('is-invalid');
    form.find('.invalid-feedback').remove();
    const password1 = $('.register-form-student #id_password1').val()
    const password2 = $('.register-form-student #id_password2').val()
    const booknumber = $('.register-form-student #id_booknumber').val()
    
    const url = $(".register-form-student").attr("data-url");

    $.ajax({
        type: 'post',
        data: {
        
            "password1": password1,
            "password2": password2,
            "booknumber": booknumber,
            "csrfmiddlewaretoken": getCookie('csrftoken'),
        },
 
        url: url,
        dataType: 'json',
        success: function (data){
            if (data['success']){
                $('.register-form-student').hide()
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


$(document).ready(function() {
    $('.register-form-customer').on('submit', function (event){
        $('#register-form__error').text('')
        event.preventDefault();
        var form = $(this);
        form.find('.is-invalid').removeClass('is-invalid');
        form.find('.invalid-feedback').remove();

        const last_name = $('.register-form-customer #id_last_name').val()
        const first_name = $('.register-form-customer #id_first_name').val()
        const patronymic = $('.register-form-customer #id_patronymic').val()
        const email = $('.register-form-customer #id_email').val()
        const customer = $('.register-form-customer #id_customer').val()
        const post = $('.register-form-customer #id_post').val()
        const password1 = $('.register-form-customer #id_password1').val()
        const password2 = $('.register-form-customer #id_password2').val()
        
        const url = $(".register-form-customer").attr("data-url");
    
        $.ajax({
            type: 'post',
            data: {
                "last_name": last_name,
                "first_name": first_name,
                "patronymic": patronymic,
                "email": email,
                "customer": customer,
                "post": post,
                "password1": password1,
                "password2": password2,
                "csrfmiddlewaretoken": getCookie('csrftoken'),
            },
     
            url: url,
            dataType: 'json',
            success: function (data){
                if (data['success']){
                    $('.register-form-customer').hide()
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
