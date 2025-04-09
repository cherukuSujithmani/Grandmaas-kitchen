document.addEventListener("DOMContentLoaded", function () {
    // Remove from wishlist
    document.querySelectorAll(".remove-btn").forEach(button => {
        button.addEventListener("click", function () {
            let productId = this.dataset.productId;
            fetch(`/wishlist/remove/${productId}/`, { method: "GET" })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload(); // Reload to update UI
                    } else {
                        alert("Error: " + data.message);
                    }
                });
        });
    });
});
