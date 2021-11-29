/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// get stripe key, removing the quotation mark characters
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
// create stripe variable 
var stripe = Stripe(stripePublicKey);
// Use stripe variable to get stripe elements 
var elements = stripe.elements();
// copy style from (https://stripe.com/docs/js/payment_request/events/on_shipping_option_change#:~:text=94941%27%2C%0A%20%20country%3A%20%27US%27%2C%0A%7D-,The%20Style%20object,-Elements%20are%20styled)
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
// use elements to create card with style from above
var card = elements.create('card', {style: style});
// mount the card to the div we made previously 
card.mount('#card-element');


// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    // add listener to card element and check for errors everytime it changes 
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        // If there are, display them in the card errors div 
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        // otherwise it will be blank 
        errorDiv.textContent = '';
    }
});

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    // prevent the default action, which here is Post 
    ev.preventDefault();
    // disable card element and submit button to prevent multiple submissions 
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    // Call confirm card payment method 
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    // execute this function on the result of confirmCardPayment 
    }).then(function(result) {
        // If there's an error put it into the card error div 
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            // Enable card element and submit button to allow users to fix error 
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {
            // If the status of payment intent comes back as succeeded, submit the fprm 
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});