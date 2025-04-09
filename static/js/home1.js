document.addEventListener("DOMContentLoaded", function () {
    let profileDropdown = document.getElementById("profileDropdown");
    let profileMenu = document.getElementById("profileMenu");

    profileDropdown.addEventListener("click", function (event) {
        event.preventDefault();
        profileMenu.classList.toggle("show");
    });

    document.addEventListener("click", function (event) {
        if (!profileDropdown.contains(event.target) && !profileMenu.contains(event.target)) {
            profileMenu.classList.remove("show");
        }
    });
});
