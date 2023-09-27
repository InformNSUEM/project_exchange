
$(document).ready(function() {
    var ajax_post = $('.post').attr("src");
    var ajax_get = $('.get').attr("src");
    var ajax_requests = $('.requests').attr("src");
 
    $('.list-group a').click(function(event) {
   
      event.preventDefault();
      var tabId = $(this).attr('href');
    
      $('.list-group a').removeClass('active');
      $(this).addClass('active')
  
      // Отправляем AJAX-запрос на сервер для получения данных для вкладки
      $.ajax({
        url: 'https://birzha.nsuem.ru/system/profile/' + tabId.slice(1) + '/',
        type: 'GET',
        dataType: 'html',
        success: function(response) {
          // Обновляем содержимое вкладки на странице
          $(".card").html(response);

          if (tabId.slice(1) == 'post_request') {
            $('.post_request').remove();

            var script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js';
            script.className = "post_request"
            document.body.appendChild(script);

            $('.select2').remove();
            var script = document.createElement('script');
            script.innerHTML = `
            $(document).ready(function() {
              $('.js-example-basic-multiple').select2({
                closeOnSelect: false});
            });`
      
            script.className = "select2";
            document.body.appendChild(script);
                 
            $('.post').remove();
            var script = document.createElement('script');
            script.src = ajax_post;
            script.className = "post";
            document.body.appendChild(script);
          }


        
        if (tabId.slice(1) == 'my_requests') {
          $('.requests').remove();
          var script = document.createElement('script');
          script.src = ajax_requests;
          script.className = "requests"
          document.body.appendChild(script);
        }
          
      
        },
        error: function(xhr, errmsg, err) {
          console.log(xhr.status + ": " + xhr.responseText);
        }
      });
    });
  });




