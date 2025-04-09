document.addEventListener("DOMContentLoaded", function () {
    // === CART FUNCTIONALITY ===
    const cartForms = document.querySelectorAll(".product-card form");

    cartForms.forEach((form) => {
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            const formData = new FormData(form);
            const url = form.action;

            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        showCartPopup("🛒 Item added to cart!");
                    } else {
                        showCartPopup("⚠️ Failed to add item.");
                    }
                })
                .catch((error) => {
                    console.error("Cart Error:", error);
                    showCartPopup("❌ Something went wrong.");
                });
        });
    });

    // === WISHLIST FUNCTIONALITY ===
    document.querySelectorAll(".wishlist-btn").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            let productId = this.dataset.productId;

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

// === POPUP FUNCTIONS ===
function showCartPopup(message) {
    const popup = document.getElementById("cart-popup");

    if (!popup) return;

    popup.innerText = message;
    popup.classList.add("show");
    popup.style.display = "block";

    setTimeout(() => {
        popup.classList.remove("show");
        popup.style.display = "none";
    }, 3000);
}

function showWishlistPopup(message) {
    const popup = document.getElementById("wishlist-popup");

    if (!popup) return;

    popup.innerText = message;
    popup.classList.add("show");
    popup.style.display = "block";

    setTimeout(() => {
        popup.classList.remove("show");
        popup.style.display = "none";
    }, 3000);
}
