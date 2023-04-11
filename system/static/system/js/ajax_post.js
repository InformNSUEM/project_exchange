$(document).ready(function() {
    $('.customer_request').on('submit', function (event){
      //$('#register-form__error').text('')
      event.preventDefault();
      var form = $(this);
      form.find('.is-invalid').removeClass('is-invalid');
      form.find('.invalid-feedback').remove();
    
      const url = $(".customer_request").attr("data-url");
      console.log(url)
    
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