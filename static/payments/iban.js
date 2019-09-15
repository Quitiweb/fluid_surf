(function($) {
    var stripe = Stripe('pk_test_53ciwitrIAzUGwCncznmkxWN00CYFVxjyL');
    var elements = stripe.elements();

    // Custom styling can be passed to options when creating an Element
    var style = {
        base: {
            fontSize: '26px',
            color: "#32325d",
        }
    };

    var options = {
        style: style,
        supportedCountries: ['SEPA'],
        placeholderCountry: 'ES',
    }

    // Create an instance of the iban Element
    var iban = elements.create('iban', options);

    // Add an instance of the iban Element into the iban-element <div>
    if($('#iban-element').length == 0) {
        iban.mount('#iban-element');
    }


    // Error message
    iban.on('change', function(event) {
        var displayError = document.getElementById('error-message');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });


    // Create a source or display an error when the form is submitted
    var form = document.getElementById('payment-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        var sourceData = {
            type: 'sepa_debit',
            currency: 'eur',
            owner: {
                name: document.querySelector('input[name="name"]').value,
                email: document.querySelector('input[name="email"]').value,
            },
            mandate: {
                // Automatically send a mandate notification email to your customer
                // once the source is charged
                notification_method: 'email',
            },
        };

        // Call stripe.createSource with the IBAN Element and additional options
        stripe.createSource(iban, sourceData).then(function(result) {
            if (result.error) {
                // Inform the customer that there was an error.
                var errorElement = document.getElementById('error-message');
                errorElement.textContent = result.error.message;
            } else {
                // Send the Source to your server.
                stripeSourceHandler(result.source);
            }
        });
    });


    // Submit the Source and the rest of your form to your server
    function stripeSourceHandler(source) {
        // Insert the Source ID into the form so it gets submitted to the server
        var form = document.getElementById('payment-form');
        var hiddenInput = document.createElement('input');

        hiddenInput.setAttribute('type', 'hidden');
        hiddenInput.setAttribute('name', 'stripeSource');
        hiddenInput.setAttribute('value', source.id);
        form.appendChild(hiddenInput);

        // Submit the form
        form.submit();
    }

})(jQuery);
