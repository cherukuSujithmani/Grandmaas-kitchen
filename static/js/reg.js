document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("register-form");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const username = document.getElementById("id_username").value.trim();
        const email = document.getElementById("id_email").value.trim();
        const password = document.getElementById("id_password").value.trim();
        const phone = document.getElementById("id_phone").value.trim();

        if (username === "" || email === "" || password === "" || phone === "") {
            alert("Please fill in all required fields.");
            return;
        }

        if (!validateEmail(email)) {
            alert("Please enter a valid email.");
            return;
        }

        if (password.length < 6) {
            alert("Password must be at least 6 characters.");
            return;
        }

        // Simulate a successful registration (replace with actual form submission logic)
        showSuccessPopup();

        setTimeout(() => {
            form.submit(); // Submit the form after showing the popup
        }, 2000); // Delay to allow the popup to be seen
    });

    function validateEmail(email) {
        const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return re.test(email);
    }

    function showSuccessPopup() {
        const popup = document.createElement("div");
        popup.className = "success-popup";
        popup.innerHTML = "Registration was successful! Redirecting...";
        document.body.appendChild(popup);

        setTimeout(() => {
            popup.style.opacity = "0";
            setTimeout(() => popup.remove(), 500);
        }, 1500);
    }
});
