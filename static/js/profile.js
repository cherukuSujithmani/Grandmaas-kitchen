function showSection(sectionId) {
    const sections = document.querySelectorAll('.profile-section');
    sections.forEach(section => {
        section.classList.add('hidden');
    });

    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.classList.remove('hidden');
    }

    // Optional: Highlight the selected tab (li)
    const sidebarLinks = document.querySelectorAll('.sidebar ul li');
    sidebarLinks.forEach(link => link.classList.remove('active-tab'));
    const clickedTab = Array.from(sidebarLinks).find(link => link.getAttribute('onclick')?.includes(sectionId));
    if (clickedTab) clickedTab.classList.add('active-tab');
}

// Optional: Auto show first section on load
document.addEventListener("DOMContentLoaded", function () {
    showSection('orders'); // or 'edit-profile' or 'wishlist'
});

// Show Add Address form
function showAddressForm() {
    fetch("/profile/add-address/")
        .then(response => response.text())
        .then(html => {
            const formContainer = document.getElementById("address-form-container");
            formContainer.innerHTML = html;
            formContainer.classList.remove("hidden");
        });
}

// Show Edit Address form
function editAddress(addressId) {
    fetch(`/profile/edit-address/${addressId}/`)
        .then(response => response.text())
        .then(html => {
            const formContainer = document.getElementById("address-form-container");
            formContainer.innerHTML = html;
            formContainer.classList.remove("hidden");
        });
}

// Show confirm "Are you sure?" on Delete
function showConfirm(btn) {
    const group = btn.closest('.btn-group');
    btn.style.display = 'none'; // Hide the Delete button
    group.querySelector('.confirm-group').classList.add('show');
}

function cancelConfirm(btn) {
    const group = btn.closest('.confirm-group');
    group.classList.remove('show');
    group.parentElement.querySelector('button[type="button"]').style.display = 'inline-block';
}


