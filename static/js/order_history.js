document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll(".order-table tbody tr");

    rows.forEach((row, index) => {
        setTimeout(() => {
            row.classList.add("fade-in");
        }, index * 200);
    });
});
