let savedData = [
    {
        id: 1,
        name: "Summer Vibes",
        author: "Masa",
        image: "../static/images/img1.jfif",
        dateAdded: "2025-08-01",
        likes: 23,
        liked: false,
        rating: null
    },
    {
        id: 2,
        name: "Chill Beats",
        author: "Dusan",
        image: "../static/images/img3.jfif",
        dateAdded: "2025-08-03",
        likes: 10,
        liked: false,
        rating: null
    },
    {
        id: 3,
        name: "Workout Pump",
        author: "Nikola",
        image: "../static/images/img4.jfif",
        dateAdded: "2025-08-05",
        likes: 45,
        liked: false,
        rating: null
    },
    {
        id: 4,
        name: "Night Drive",
        author: "Ana",
        image: "../static/images/img2.jpg",
        dateAdded: "2025-08-07",
        likes: 17,
        liked: false,
        rating: null
    },
    {
        id: 5,
        name: "Morning Energy",
        author: "Marko",
        image: "../static/images/img5.jfif",
        dateAdded: "2025-08-08",
        likes: 30,
        liked: false,
        rating: null
    },
    {
        id: 6,
        name: "Focus Beats",
        author: "Jelena",
        image: "../static/images/img6.jfif",
        dateAdded: "2025-08-09",
        likes: 12,
        liked: false,
        rating: null
    },
    {
        id: 7,
        name: "Throwback Classics",
        author: "Milos",
        image: "../static/images/img7.jfif",
        dateAdded: "2025-08-10",
        likes: 50,
        liked: false,
        rating: null
    }
];

const currentUser = "user123";
const userLikesKey = `likes_${currentUser}`;
const userRatingsKey = `ratings_${currentUser}`;
let userLikes = JSON.parse(localStorage.getItem(userLikesKey)) || {};
let userRatings = JSON.parse(localStorage.getItem(userRatingsKey)) || {};
function saveData() {
    localStorage.setItem("trendingData", JSON.stringify(savedData));
}

function renderTrending() {
    const listEl = document.getElementById("trending-list");
    listEl.innerHTML = "";

    savedData.forEach(pl => {
        const card = document.createElement("div");
        card.className = "playlist-card";

        card.innerHTML = `
    <img src="${pl.image}" alt="cover">
    <div class="playlist-info">
        <h3>${pl.name}</h3>
        <p>By ${pl.author}</p>
        <p>Added: ${pl.dateAdded}</p>
    </div>
    <div class="playlist-actions">
        <button class="like-btn ${userLikes[pl.id] ? 'liked' : ''}" 
                aria-pressed="${userLikes[pl.id] ? 'true' : 'false'}" 
                style="opacity: ${userLikes[pl.id] ? 1 : 0.4};">
            ❤️ ${pl.likes}
        </button>
        <div class="rating-display" tabindex="0" aria-label="Ocena plejlistu" data-playlist-id="${pl.id}" 
             style="opacity: ${userRatings[pl.id] ? 1 : 0.4};">
            <span class="star-icon">⭐</span>
            <span class="rating-value">${userRatings[pl.id] ? userRatings[pl.id].toFixed(1) : "N/A"}</span>
        </div>
    </div>
`;

        card.querySelector(".like-btn").addEventListener("click", () => {
            const liked = userLikes[pl.id] || false;
            userLikes[pl.id] = !liked;

            if (userLikes[pl.id]) {
                pl.likes += 1;
            } else {
                pl.likes -= 1;
            }

            localStorage.setItem(userLikesKey, JSON.stringify(userLikes));
            saveData();
            renderTrending();
        });


        listEl.appendChild(card);
    });

    document.querySelectorAll('.rating-display').forEach(ratingEl => {
        ratingEl.addEventListener('click', () => {
            const playlistId = parseInt(ratingEl.dataset.playlistId);
            const pl = savedData.find(p => p.id === playlistId);
            if (!pl) return;
            openRatingModal(pl);
        });
    });
}

const ratingModalHTML = `
  <div id="rating-modal" class="rating-modal" hidden>
    <div class="rating-modal-content" role="dialog" aria-modal="true" aria-labelledby="rating-modal-title">
      <h2 id="rating-modal-title">Rate playlist!</h2>
      <div class="rating-stars">
        ${Array.from({ length: 10 }, (_, i) => `<span class="star" data-value="${i + 1}" aria-label="${i + 1} zvezdica" role="button" tabindex="0">☆</span>`).join('')}
      </div>
      <button id="cancel-rating-btn" aria-label="Cancel your rating">Cancel your rating</button>
      <button id="rating-modal-close" aria-label="Zatvori modal">X</button>
    </div>
  </div>
`;

document.body.insertAdjacentHTML('beforeend', ratingModalHTML);

const ratingModal = document.getElementById('rating-modal');
const ratingStars = ratingModal.querySelectorAll('.star');
const ratingModalCloseBtn = document.getElementById('rating-modal-close');

let currentPlaylist = null;

function openRatingModal(pl) {
    currentPlaylist = pl;
    ratingModal.hidden = false;
    highlightStars(pl.rating || 0);
    ratingStars[0].focus();
    document.body.style.overflow = 'hidden'; 
}

function closeRatingModal() {
    ratingModal.hidden = true;
    currentPlaylist = null;
    document.body.style.overflow = '';
}

function highlightStars(rating) {
    ratingStars.forEach(star => {
        const val = Number(star.dataset.value);
        if (val <= rating) {
            star.textContent = '⭐';
            star.classList.add('selected');
            star.style.opacity = '1'; 
            star.style.color = 'gold'; 
        } else {
            star.textContent = '⭐';
            star.classList.remove('selected');
            star.style.opacity = '0.3';
            star.style.color = 'gold';
        }
    });
}

ratingStars.forEach(star => {
    star.addEventListener('click', () => {
        if (!currentPlaylist) return;
        const rating = Number(star.dataset.value);

        userRatings[currentPlaylist.id] = rating;   
        currentPlaylist.rating = rating;            

        localStorage.setItem(userRatingsKey, JSON.stringify(userRatings));
        saveData();
        renderTrending();
        closeRatingModal();
    });


    star.addEventListener('mouseenter', () => {
        highlightStars(Number(star.dataset.value));
    });

    star.addEventListener('mouseleave', () => {
        if (!currentPlaylist) return;
        highlightStars(currentPlaylist.rating || 0);
    });
});

ratingModalCloseBtn.addEventListener('click', closeRatingModal);
ratingModal.addEventListener('click', (e) => {
    if (e.target === ratingModal) {
        closeRatingModal();
    }
});

renderTrending(); 
const trendingTitle = document.getElementById("collab-name");
const scrollText = document.getElementById("scroll-text");

window.addEventListener("scroll", () => {
    const scrollY = window.scrollY;
    const fadeSpeed = 200;

    let opacity = 1 - scrollY / fadeSpeed;
    if (opacity < 0) opacity = 0;
    if (opacity > 1) opacity = 1;

    trendingTitle.style.opacity = opacity;
    scrollText.style.opacity = opacity;
});

const cancelRatingBtn = document.getElementById('cancel-rating-btn');

cancelRatingBtn.addEventListener('click', () => {
    if (!currentPlaylist) return;
    
    delete userRatings[currentPlaylist.id];
    currentPlaylist.rating = null;

    localStorage.setItem(userRatingsKey, JSON.stringify(userRatings));
    saveData();
    renderTrending();
    closeRatingModal();
});
