
const sectionTitles = {
    'home': 'Dashboard',
    'users': 'User Management',
    'trending': 'Trending Playlists',
    'purchases': 'Purchases'
};

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

document.addEventListener('DOMContentLoaded', function() {
    showSection('home');
});