const SPOTIFY_CLIENT_ID = '172aabf79532439381a63f40f6aa175f';
const SPOTIFY_CLIENT_SECRET = '73cde19a90ae4582a2c1e066944e7276';

const playlistKey = 'collab_playlist_v1';
const members = ['Dusan', 'Masa', 'Nikola'];

const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
const searchStatus = document.getElementById('search-status');
const playlistEl = document.getElementById('playlist');
const playlistCount = document.getElementById('playlist-count');
const userSelect = document.getElementById('user-select');
console.log('searchResults element:', searchResults);
let token = null;
let tokenExpiry = 0;
let playlist = JSON.parse(localStorage.getItem(playlistKey)) || [];
let searchTimeout = null;

function savePlaylist() {
    localStorage.setItem(playlistKey, JSON.stringify(playlist));
}

function formatDuration(ms) {
    const s = Math.floor(ms / 1000);
    const m = Math.floor(s / 60);
    const rem = s % 60;
    return `${m}:${rem.toString().padStart(2, '0')}`;
}

async function getToken(force = false) {
    const now = Date.now();
    if (!force && token && tokenExpiry > now + 10000) return;

    if (!SPOTIFY_CLIENT_ID || !SPOTIFY_CLIENT_SECRET) {
        console.warn('Spotify credentials missing');
        return;
    }
    const credentials = btoa(`${SPOTIFY_CLIENT_ID}:${SPOTIFY_CLIENT_SECRET}`);
    try {
        const res = await fetch('https://accounts.spotify.com/api/token', {
            method: 'POST',
            headers: {
                Authorization: `Basic ${credentials}`,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'grant_type=client_credentials',
        });
        if (!res.ok) throw new Error('Failed to get token');
        const data = await res.json();
        token = data.access_token;
        tokenExpiry = Date.now() + data.expires_in * 1000;
    } catch (e) {
        console.error(e);
    }
}

async function searchSpotify(query) {
    if (!token) {
        await getToken(true);
        if (!token) return;
    }

    const params = new URLSearchParams({ q: query, type: 'track', limit: '8' });
    try {
        searchStatus.textContent = 'Loading...';
        const res = await fetch(`https://api.spotify.com/v1/search?${params}`, {
            headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error('Search failed');
        const data = await res.json();
        renderSearchResults(data.tracks.items);
    } catch (e) {
        console.error(e);
        searchStatus.textContent = 'Error fetching results';
    } finally {
        searchStatus.textContent = '';
    }
}

function renderSearchResults(tracks) {
    console.log('renderSearchResults called with:', tracks);
    const searchResults = document.getElementById("search-results");

    if (!tracks || tracks.length === 0) {
        searchResults.style.display = "none"; 
        searchResults.innerHTML = "";
        return;
    }

    searchResults.style.display = "block"; 
    searchResults.innerHTML = '';

    tracks.forEach(track => {
        const li = document.createElement('li');
        li.className = 'search-suggestion-item';
        li.style.cursor = 'pointer';
        li.addEventListener('click', () => {
            addToPlaylist(track);
            clearSearch();
        });

        const img = document.createElement('img');
        img.src = track.album.images?.[0]?.url || '';
        img.alt = 'cover';
        img.width = 40;
        img.height = 40;
        img.className = 'imgSearchCover';

        const textDiv = document.createElement('div');
        textDiv.className = 'search-suggestion-text';

        const strong = document.createElement('strong');
        strong.textContent = track.name;

        const small = document.createElement('small');
        small.textContent = track.artists.map(a => a.name).join(', ');

        textDiv.appendChild(strong);
        textDiv.appendChild(document.createTextNode(' - '));
        textDiv.appendChild(small);

        li.appendChild(img);
        li.appendChild(textDiv);

        searchResults.appendChild(li);
    });
}




function addToPlaylist(track) {
    const addedBy = userSelect.value;
    const entry = {
        id: track.id,
        name: track.name,
        artists: track.artists.map(a => a.name).join(', '),
        duration_ms: track.duration_ms,
        spotify_url: track.external_urls.spotify,
        image: track.album.images[0]?.url || '',
        addedBy,
        addedAt: Date.now(),
    };
    playlist.unshift(entry);
    savePlaylist();
    renderPlaylist();
}

function removeFromPlaylist(id) {
    playlist = playlist.filter(item => item.id !== id);
    savePlaylist();
    renderPlaylist();
}

function renderPlaylist() {
    playlistEl.innerHTML = '';
    playlistCount.textContent = playlist.length;

    if (playlist.length === 0) {
        const p = document.createElement('p');
        p.textContent = 'Empty — You can add songs from search.';
        playlistEl.appendChild(p);
        return;
    }

    playlist.forEach(item => {
        const li = document.createElement('li');
        li.classList.add('playlist-item');

        const link = document.createElement('a');
        link.href = item.spotify_url;
        link.target = '_blank';
        link.rel = 'noreferrer';
        link.classList.add('item-link-a');

        const img = document.createElement('img');
        img.src = item.image;
        img.alt = 'cover';
        img.style.width = '50px';
        img.style.height = '50px';

        const infoDiv = document.createElement('div');
        infoDiv.style.display = 'inline-block';
        infoDiv.style.marginLeft = '10px';

        const strong = document.createElement('strong');
        strong.textContent = item.name;

        const p = document.createElement('p');
        p.textContent = `${item.artists} • ${formatDuration(item.duration_ms)}`;

        const small = document.createElement('small');
        small.textContent = `Added: ${item.addedBy}`;

        infoDiv.appendChild(strong);
        infoDiv.appendChild(p);
        infoDiv.appendChild(small);

        link.appendChild(img);
        link.appendChild(infoDiv);

        const btnDiv = document.createElement('div');
        const btn = document.createElement('button');
        btn.textContent = 'Remove';
        btn.classList.add('remove-btn');
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            removeFromPlaylist(item.id);
        });

        btnDiv.appendChild(btn);

        li.appendChild(link);
        li.appendChild(btnDiv);
        playlistEl.appendChild(li);
    });
}

searchInput.addEventListener('input', () => {
  const query = searchInput.value.trim();

  if (searchTimeout) clearTimeout(searchTimeout);

  if (!query) {
    clearSearch();
    searchStatus.textContent = '';
    searchResults.style.display = 'none';  
    return;
  }

  searchTimeout = setTimeout(async () => {
    searchStatus.textContent = 'Loading...';
    await searchSpotify(query);
    searchStatus.textContent = '';
    if (searchResults.children.length > 0) {
      searchResults.style.display = 'block';
    } else {
      searchResults.style.display = 'none'; 
    }
  }, 350);
});

function clearSearch() {
  searchResults.innerHTML = '';
  searchInput.value = '';
  searchResults.style.display = 'none';
}


renderPlaylist();
getToken();

document.getElementById('trending-btn').addEventListener('click', () => {
    window.location.href = '/trending';
});
document.getElementById('login-btn').addEventListener('click', () => {
    window.location.href = '/login';
});
document.getElementById('premium-btn').addEventListener('click', () => {
    window.location.href = '/pricing';
});
