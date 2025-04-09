document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    const passwordField = document.getElementById("id_password");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const username = document.getElementById("id_username").value.trim();
        const password = passwordField.value.trim();

        if (username === "" || password === "") {
            alert("Please fill in all fields.");
            return;
        }

        // Show success popup
        showSuccessPopup();

        setTimeout(() => {
            form.submit(); // Submit the form after showing the popup
        }, 1500);
    });

    function showSuccessPopup() {
        const popup = document.createElement("div");
        popup.className = "success-popup";
        popup.innerHTML = "Login successful! Redirecting...";
        document.body.appendChild(popup);

        setTimeout(() => {
            popup.style.opacity = "0";
            setTimeout(() => popup.remove(), 500);
        }, 1200);
    }

    // Show/Hide Password Feature
    const toggleBtn = document.createElement("button");
    toggleBtn.type = "button";
    toggleBtn.className = "toggle-password";
    toggleBtn.innerText = "👁";
    passwordField.parentNode.appendChild(toggleBtn);

    toggleBtn.addEventListener("click", function () {
        if (passwordField.type === "password") {
            passwordField.type = "text";
            toggleBtn.innerText = "🙈";
        } else {
            passwordField.type = "password";
            toggleBtn.innerText = "👁";
        }
    });
});
