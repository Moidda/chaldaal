// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
    'use strict'

    window.addEventListener('load', function () {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation')

    // Loop over them and prevent submission
    Array.prototype.filter.call(forms, function (form) {
        form.addEventListener('submit', function (event) {
            var validated = form.checkValidity();

            var radioBtns = document.getElementsByName("paymentMethod");
            var paymentMethod;
            for(var i = 0; i < radioBtns.length; i++)
                if(radioBtns[i].checked)
                    paymentMethod = radioBtns[i].value;

            var username = document.getElementById("username");
            console.log(paymentMethod);
            console.log(username.value);

            document.getElementById("username").required = Boolean(paymentMethod == "credit_card");
            document.getElementById("bank").required = Boolean(paymentMethod == "credit_card");
            document.getElementById("card_type").required = Boolean(paymentMethod == "credit_card");
            document.getElementById("card_no").required = Boolean(paymentMethod == "credit_card");

            document.getElementById("bkash_phone_no").required = Boolean(paymentMethod == "bkash");

            // fetch all the elements that are of type input
            // if any element is required but has no value, form is invalid
            var inputElements = document.getElementsByTagName("input");
            for(var i = 0; i < inputElements.length; i++)
                if(inputElements[i].required && !Boolean(inputElements[i].value))
                    validated = false;

            if (validated === false) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated')
        }, false)
        })
    }, false)
})()