document.addEventListener("DOMContentLoaded", function () {

    // Handle Add to Cart with animation + AJAX
    document.querySelectorAll(".cart-form").forEach(form => {
        form.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent form from reloading the page

            const productId = this.querySelector(".wishlist-btn").dataset.productId;
            const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/add_to_cart/${productId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showCartPopup("🛒 Item added to cart!");
                    } else {
                        showCartPopup("⚠️ Could not add to cart.");
                    }
                })
                .catch(error => {
                    console.error("Cart Error:", error);
                    showCartPopup("❌ Something went wrong.");
                });
        });
    });

    // Handle Wishlist button clicks
    document.querySelectorAll(".wishlist-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            const productId = this.dataset.productId;

            fetch(`/wishlist/add/${productId}/`, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
                .then(response => response.json())
                .then(data => {
                    showWishlistPopup(data.message || "💖 Added to wishlist!");
                })
                .catch(error => {
                    console.error("Wishlist Error:", error);
                    showWishlistPopup("❌ Could not add to wishlist.");
                });
        });
    });

});

// Show Cart Popup
function showCartPopup(message) {
    const popup = document.getElementById("cart-popup");

    if (!popup) {
        console.error("Cart popup not found!");
        return;
    }

    popup.innerText = message;
    popup.classList.add("show");

    setTimeout(() => {
        popup.classList.remove("show");
    }, 3000);
}

// Show Wishlist Popup
function showWishlistPopup(message) {
    const popup = document.getElementById("wishlist-popup");

    if (!popup) {
        console.error("Wishlist popup not found!");
        return;
    }

    popup.innerText = message;
    popup.classList.add("show");

    setTimeout(() => {
        popup.classList.remove("show");
    }, 3000);
}
