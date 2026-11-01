// The color theme is controlled by prefers-color-scheme in CSS.
// Native <details> keeps navigation usable without JavaScript.

const navigationDetails = document.querySelectorAll(
    ".site-header .nav-group, .site-header .mobile-menu",
);

function closeNavigation(details, restoreFocus = false) {
    details.querySelectorAll("details[open]").forEach((child) => {
        child.open = false;
    });

    details.open = false;

    if (restoreFocus) {
        details.querySelector(":scope > summary")?.focus();
    }
}

function closeMenusOutside(event) {
    const path =
        typeof event.composedPath === "function" ? event.composedPath() : [];

    const openMenus = document.querySelectorAll(
        ".site-header .nav-group[open], .site-header .mobile-menu[open]",
    );

    openMenus.forEach((details) => {
        const isInside =
            path.includes(details) ||
            (event.target instanceof Node && details.contains(event.target));

        if (!isInside) {
            closeNavigation(details);
        }
    });
}

// Catch outside presses before other elements can stop propagation.
// Presses inside the menu retain their normal link/toggle behavior.
document.addEventListener("pointerdown", closeMenusOutside, true);

// Also support keyboard-generated clicks.
document.addEventListener("click", closeMenusOutside, true);

// Escape closes the nearest open menu and focuses its summary.
document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || !(event.target instanceof Element)) {
        return;
    }

    const details = event.target.closest(
        ".nav-group[open], .mobile-menu[open]",
    );

    if (details) {
        event.preventDefault();
        closeNavigation(details, true);
    }
});

// Close when focus moves to another element outside the menu.
// Avoid closing on blur, which can interrupt link clicks in Safari.
document.addEventListener("focusin", (event) => {
    if (!(event.target instanceof Element)) {
        return;
    }

    navigationDetails.forEach((details) => {
        if (details.open && !details.contains(event.target)) {
            closeNavigation(details);
        }
    });
});

// Reset nested submenus when the main mobile menu closes.
document.querySelectorAll(".mobile-menu").forEach((menu) => {
    menu.addEventListener("toggle", () => {
        if (!menu.open) {
            menu.querySelectorAll("details[open]").forEach((details) => {
                details.open = false;
            });
        }
    });
});
