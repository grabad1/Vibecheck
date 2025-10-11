const SPOTIFY_CLIENT_ID = '172aabf79532439381a63f40f6aa175f';
const SPOTIFY_CLIENT_SECRET = '73cde19a90ae4582a2c1e066944e7276';

const input = document.getElementById("search-input");
const resultsDiv = document.getElementById("search-results");
let timeout = null;

input.addEventListener("input", () => {
  clearTimeout(timeout);
  const query = input.value.trim();
  if (!query) {
    resultsDiv.innerHTML = "";
    resultsDiv.style.display = "none";
    return;
  }

  timeout = setTimeout(() => {
  const collabId = document.body.dataset.collabId;
  fetch(`/search/${collabId}?q=${encodeURIComponent(query)}`)
    .then(res => res.text())
    .then(html => {
      resultsDiv.innerHTML = html;
      resultsDiv.style.display = "block";
    })
    .catch(err => console.error(err));
}, 300);
});


document.querySelectorAll('.track-form').forEach(form => {
  form.addEventListener('click', function(e) {
    e.preventDefault();
    form.submit();
  });
});


document.getElementById('trending-btn').addEventListener('click', () => {
    window.location.href = '/trending';
});
document.getElementById('login-btn').addEventListener('click', () => {
    window.location.href = '/login';
});
document.getElementById('premium-btn').addEventListener('click', () => {
    window.location.href = '/pricing';
});
