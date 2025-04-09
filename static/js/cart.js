document.addEventListener("DOMContentLoaded", function () {
    // Popup Message Function
    function showPopup(message) {
        let popup = document.getElementById("popup-message");
        popup.innerText = message;
        popup.style.display = "block";

        setTimeout(() => {
            popup.style.display = "none";
        }, 3000);
    }

    // Handle Quantity Update
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", function (event) {
            event.preventDefault();  // Prevent default form submission
            let formData = new FormData(this);

            fetch(this.action, {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showPopup("Cart updated!");
                    location.reload();  // Refresh to update subtotal & total
                }
            })
            .catch(error => console.log(error));
        });
    });

    // Handle Remove Button Click
    document.querySelectorAll(".btn").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            let url = this.href;

            fetch(url, { method: "GET" })
                .then(response => {
                    if (response.ok) {
                        this.closest("tr").remove();
                        showPopup("Item removed from cart!");
                        setTimeout(() => location.reload(), 1000);
                    }
                })
                .catch(error => console.log(error));
        });
    });

    // Handle Checkout Button Click
    let checkoutBtn = document.querySelector(".checkout-btn");
    if (checkoutBtn) {
        checkoutBtn.addEventListener("click", function (event) {
            event.preventDefault();
            showPopup("Proceeding to checkout...");
            setTimeout(() => {
                window.location.href = this.href;
            }, 1000);
        });
    }
});
