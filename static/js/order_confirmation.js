// order_confirmation.js
document.addEventListener("DOMContentLoaded", function () {
    let popup = document.getElementById("order-popup");
    let closeBtn = document.getElementById("close-popup");

    // Show popup when page loads
    popup.style.display = "flex";

    // Close popup when button is clicked
    closeBtn.addEventListener("click", function () {
        popup.style.display = "none";
    });
});
