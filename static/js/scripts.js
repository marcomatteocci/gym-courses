(function () {
    "use strict";

    // Aggiungo la classe 'scrolled' al body quando l'utente scrolla la pagina
    function handleScroll() {
        let body = document.body;
        let header = document.querySelector("#header");
        let stickyClasses = ["scroll-up-sticky", "sticky-top", "fixed-top"];
        let isSticky = stickyClasses.some(stickyClass => header.classList.contains(stickyClass));
        if (isSticky) {
            body.classList.toggle("scrolled", window.scrollY > 20);
        }
    }

    // Aggiungo la classe 'mob-nav-active' al body quando l'utente clicca sul pulsante di navigazione mobile
    let mobileNavToggle = document.querySelector(".mob-nav-toggle");
    document.addEventListener("scroll", handleScroll);
    window.addEventListener("load", handleScroll);
    if (mobileNavToggle) {
        mobileNavToggle.addEventListener("click", function toggleMobileNav() {
            let body = document.body;
            body.classList.toggle("mob-nav-active");
            mobileNavToggle.classList.toggle("bi-list");
            mobileNavToggle.classList.toggle("bi-x");
        });
    }
})();
