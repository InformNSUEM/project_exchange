$(document).ready(function() {
 
    $('.requests_body a').click(function(event) {

      event.preventDefault();

      var url = $(this).attr('href');

      // Отправляем AJAX-запрос на сервер для получения данных для вкладки
      $.ajax({
        url: url,
        type: 'GET',
        dataType: 'html',
        success: function(response) {
          // Обновляем содержимое вкладки на странице
          $(".card").html(response);
        },
        error: function(xhr, errmsg, err) {
          console.log(xhr.status + ": " + xhr.responseText);
        }
      });
    });
  });