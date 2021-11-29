/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// get stripe key, removing the quotation mark characters
var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);
// create stripe variable 
var stripe = Stripe(stripe_public_key);
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