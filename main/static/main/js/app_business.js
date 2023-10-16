$(document).ready(function () {

    $("*[required]").each(function () {
        var label = $(this).prev("label");
        label.append(' <span class="required" style="color: red; font-size: 1em; margin-left: 5px;">*</span>');
    });
    
    var form = $("#business_application");
    var list_group = $(".list-group");
    var steps = form.find(".step");
    var list_item = list_group.find(".list-group-item");
    var currentStep = 0;

    $('[data-bs-toggle="tooltip"]').tooltip();

    function goToStep(step) {
      
        steps.removeClass("active").eq(step).addClass("active");
        list_item.removeClass("active").eq(step).addClass("active");
        currentStep = step;

        $('#select2Type').select2({
          closeOnSelect: false
        });

        $('#select2Depth').select2({
          closeOnSelect: false
        });

        $('#select2Programs').select2({
          closeOnSelect: false
        });
    }

    function isValidEmail(email) {
        var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        return emailPattern.test(email);
    }

    form.find(".next-step").click(function () {

        var currentStepFields = steps.eq(currentStep).find("*[required]");
        var some = $("#select2Type").val();
      
        var isValid = true;

        currentStepFields.each(function () {
            if ($(this).val() === "" || $(this).val().length == 0)  {
                isValid = false;
                $(this).addClass("is-invalid");
                $(this).next(".invalid-feedback").text("Поле обязательно для заполнения.");
            } else {
                $(this).removeClass("is-invalid");
                $(this).next(".invalid-feedback").text("");
            }
        });

        if (currentStep === 0) {
            var emailField = $("#email");
            var emailValue = emailField.val();
        
            if (!isValidEmail(emailValue)) {
                isValid = false;
                emailField.addClass("is-invalid");
                emailField.next(".invalid-feedback").text("Введите корректный email адрес.");
            } else {
                emailField.removeClass("is-invalid");
                emailField.next(".invalid-feedback").text("");
            }
        }
       

    if (isValid) {
        if (currentStep < steps.length - 1) {
            goToStep(currentStep + 1);
        }
    }
    });

    form.find(".prev-step").click(function () {
        if (currentStep > 0) {
            goToStep(currentStep - 1);
        }
    });


    $('.business_application').on('submit', function(event) {
        event.preventDefault();
        var form = $(this);
        var submitButton = document.getElementById("submitButton");
        submitButton.disabled = true;
        const url = $(".business_application").attr("data-url");
       

        $.ajax({
            type: 'post',
            data: $(this).serialize(),
            url: url,
            dataType: 'json',

            
            
            success: function (data){
               
                $("#myModal").modal("show");
                $("#value_buisness").text(data.id)
             
            },

            error: function(error) {
                console.error('Ошибка при выполнения запроса: ');
            }
        }
        )

    });
    $("#submitNew").click(function () {

        $("#myModal").modal("hide"); 
        location.reload();
     
    });

    $("#submitEnd").click(function () {

        $("#myModal").modal("hide"); 
        window.location.href = "/";
     
    });
});

