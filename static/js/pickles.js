document.addEventListener("DOMContentLoaded", function () {
    const addToCartForms = document.querySelectorAll(".add-to-cart-form");

    addToCartForms.forEach(form => {
        form.querySelector(".add-to-cart").addEventListener("click", function (event) {
            event.preventDefault(); // Prevent form submission

            const formData = new FormData(form);
            const url = form.action;

            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => {
                if (response.ok) {
                    return response.json(); // Expecting JSON response
                } else {
                    throw new Error("Network response was not ok.");
                }
            })
            .then(data => {
                showPopup(data.message || "Item added to cart!");
            })
            .catch(error => {
                console.error("Error:", error);
                showPopup("Failed to add item. Try again!");
            });
        });
    });
});


// Function to show popup notification
function showPopup(message) {
    let popup = document.createElement("div");
    popup.className = "popup";
    popup.innerText = message;
    
    document.body.appendChild(popup);
    
    // Show popup
    popup.style.display = "block";
    
    // Remove popup after 3 seconds
    setTimeout(() => {
        popup.style.display = "none";
        popup.remove();
    }, 3000);
}

// wishlist functionality
document.addEventListener("DOMContentLoaded", function () {
    // Ensure all wishlist buttons work
    document.querySelectorAll(".wishlist-btn").forEach(button => {
        button.addEventListener("click", function () {
            let productId = this.dataset.productId;

            fetch(`/wishlist/add/${productId}/`, { method: "GET" })
                .then(response => response.json())
                .then(data => {
                    showWishlistPopup(data.message);
                })
                .catch(error => console.error("Error:", error));
        });
    });
});

// Function to show wishlist popup
function showWishlistPopup(message) {
    let popup = document.getElementById("wishlist-popup");
    
    if (!popup) {
        console.error("Wishlist popup element not found!");
        return;
    }

    popup.innerText = message;
    popup.classList.add("show");

    setTimeout(() => {
        popup.classList.remove("show");
    }, 3000);
} 