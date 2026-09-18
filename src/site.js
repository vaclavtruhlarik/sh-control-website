// The color theme is intentionally controlled only by prefers-color-scheme in CSS.
// Native <details> makes mobile navigation work even with JavaScript disabled.
document.querySelectorAll('.mobile-menu a').forEach(link => {
  link.addEventListener('click', () => link.closest('details').removeAttribute('open'));
});
