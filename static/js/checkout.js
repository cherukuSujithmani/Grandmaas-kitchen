document.addEventListener("DOMContentLoaded", function () {
    const cardRadio = document.querySelector('input[value="Card"]');
    const cardDetails = document.querySelector(".card-details");

    const paymentOptions = document.querySelectorAll('input[name="payment_method"]');

    paymentOptions.forEach(input => {
        input.addEventListener("change", function () {
            if (cardRadio.checked) {
                cardDetails.style.display = "block";
            } else {
                cardDetails.style.display = "none";
            }
        });
    });
});
document.addEventListener("DOMContentLoaded", function () {
    const cardRadio = document.querySelector('input[value="Card"]');
    const cardDetails = document.querySelector(".card-details");

    const paymentOptions = document.querySelectorAll('input[name="payment_method"]');

    paymentOptions.forEach(input => {
        input.addEventListener("change", function () {
            cardDetails.style.display = cardRadio.checked ? "block" : "none";
        });
    });
});
fetch('/checkout/', {
    method: 'POST',
    body: formData,
    headers: {
        'X-CSRFToken': csrfToken
    }
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        window.location.href = `/order-confirmation/${data.order_id}/`;
    }
});
