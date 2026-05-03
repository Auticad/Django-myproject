/* main.js — script base MyProject */

// HTMX global config
document.addEventListener('DOMContentLoaded', function () {
  // Aggiungi CSRF token a tutte le richieste HTMX
  document.body.addEventListener('htmx:configRequest', function (evt) {
    const csrfToken = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];
    if (csrfToken) {
      evt.detail.headers['X-CSRFToken'] = csrfToken;
    }
  });
});
