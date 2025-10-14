//Maša Cvetanovski 2022/0128
const sectionTitles = {
    'home': 'Dashboard',
    'trending': 'Edit trending',
    'createPlaylist': 'Create Playlist',
    'myPlaylists': 'My Playlists'
};
document.addEventListener("DOMContentLoaded", function() {
    const activeSection = window.ACTIVE_SECTION || 'home';
    showSection(activeSection);
});
function showSection(sectionName) {
    const allSections = document.querySelectorAll('.section-content');
    allSections.forEach(section => {
        section.classList.remove('active');
    });

    const selectedSection = document.getElementById(sectionName + '-section');
    if (selectedSection) {
        selectedSection.classList.add('active');
    }

    const pageTitle = document.getElementById('page-title');
    if (pageTitle && sectionTitles[sectionName]) {
        pageTitle.textContent = sectionTitles[sectionName];
    }

    const allNavLinks = document.querySelectorAll('.nav-link[data-section]');
    allNavLinks.forEach(link => {
        link.classList.remove('active');
    });

    const activeNavLink = document.querySelector(`.nav-link[data-section="${sectionName}"]`);
    if (activeNavLink) {
        activeNavLink.classList.add('active');
    }
}

