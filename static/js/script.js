document.addEventListener("DOMContentLoaded", function() {
    // Navbar Toggle
    document.querySelector(".menu-toggle").addEventListener("click", function() {
        document.querySelector(".nav-links").classList.toggle("active");
    });

    // Floating Food Animation
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    function checkVisibility() {
        const container = document.getElementById("food-container");
        if (isInViewport(container)) {
            document.querySelectorAll(".food-image").forEach(img => {
                img.classList.add("visible");
            });
            window.removeEventListener("scroll", checkVisibility);
        }
    }

    window.addEventListener("scroll", checkVisibility);
    checkVisibility();    
});
document.addEventListener("DOMContentLoaded", function () {
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return rect.top < window.innerHeight && rect.bottom >= 0;
    }

    function handleScroll() {
        const floatingFoods = document.querySelectorAll(".floating-food");
        const phoneContainer = document.querySelector(".phone-container");

        floatingFoods.forEach(img => {
            if (isElementInViewport(img)) {
                img.classList.add("animate");
            }
        });

        if (isElementInViewport(phoneContainer)) {
            phoneContainer.classList.add("visible");
        }
    }

    window.addEventListener("scroll", handleScroll);
    handleScroll(); // Run on load in case already in view
});


// Just to make sure animation is removed after 2s if not already
setTimeout(() => {
    const intro = document.getElementById('intro-animation');
    if (intro) intro.style.display = 'none';
}, 3000);