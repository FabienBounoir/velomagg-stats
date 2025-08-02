// JavaScript pour VéloMAG Stats
document.addEventListener('DOMContentLoaded', function () {

    // Mise à jour de l'heure de dernière actualisation
    updateLastUpdate();

    // Chargement des statistiques
    loadStatistics();

    // Navigation smooth scroll
    setupSmoothScrolling();

    // Auto-refresh des données (toutes les 5 minutes)
    setInterval(loadStatistics, 5 * 60 * 1000);
});

/**
 * Met à jour l'affichage de la dernière mise à jour
 */
function updateLastUpdate() {
    const now = new Date();
    const lastUpdateElement = document.getElementById('last-update');
    if (lastUpdateElement) {
        lastUpdateElement.textContent = now.toLocaleString('fr-FR');
    }
}

/**
 * Charge les statistiques depuis l'API ou les fichiers locaux
 */
async function loadStatistics() {
    try {
        // Tenter de charger depuis le fichier JSON local
        const response = await fetch('data/velomagg_analysis_stats.json');
        if (response.ok) {
            const stats = await response.json();
            updateStatsDisplay(stats);
        } else {
            // Fallback: charger directement depuis l'API
            await loadFromAPI();
        }
    } catch (error) {
        console.warn('Erreur lors du chargement des statistiques:', error);
        // Afficher des valeurs par défaut
        setDefaultStats();
    }
}

/**
 * Charge les données directement depuis l'API VéloMAG
 */
async function loadFromAPI() {
    try {
        const response = await fetch('https://portail-api-data.montpellier3m.fr/bikestation');
        if (response.ok) {
            const stations = await response.json();
            const stats = calculateStats(stations);
            updateStatsDisplay(stats);
        }
    } catch (error) {
        console.warn('Erreur API:', error);
        setDefaultStats();
    }
}

/**
 * Calcule les statistiques à partir des données des stations
 */
function calculateStats(stations) {
    const totalStations = stations.length;
    const totalBikes = stations.reduce((sum, station) =>
        sum + (station.availableBikeNumber?.value || 0), 0);
    const totalSlots = stations.reduce((sum, station) =>
        sum + (station.totalSlotNumber?.value || 0), 0);
    const occupationRate = totalSlots > 0 ? (totalBikes / totalSlots * 100) : 0;

    return {
        general: {
            total_stations: totalStations,
            total_bikes: totalBikes,
            total_capacity: totalSlots,
            average_occupancy: occupationRate / 100
        }
    };
}

/**
 * Met à jour l'affichage des statistiques
 */
function updateStatsDisplay(stats) {
    if (stats && stats.general) {
        const elements = {
            'total-stations': stats.general.total_stations,
            'total-bikes': stats.general.total_bikes,
            'occupation-rate': (stats.general.average_occupancy * 100).toFixed(1) + '%'
        };

        Object.entries(elements).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                // Animation de transition
                element.style.transition = 'all 0.3s ease';
                element.style.opacity = '0.5';
                setTimeout(() => {
                    element.textContent = value;
                    element.style.opacity = '1';
                }, 150);
            }
        });

        updateLastUpdate();
    }
}

/**
 * Définit des statistiques par défaut
 */
function setDefaultStats() {
    const defaultStats = {
        general: {
            total_stations: 20,
            total_bikes: 113,
            average_occupancy: 0.426
        }
    };
    updateStatsDisplay(defaultStats);
}

/**
 * Configure le défilement fluide pour la navigation
 */
function setupSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');

    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 100;

                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });

                // Mettre à jour l'état actif de la navigation
                updateActiveNavItem(this);
            }
        });
    });
}

/**
 * Met à jour l'élément de navigation actif
 */
function updateActiveNavItem(clickedLink) {
    // Retirer la classe active de tous les liens
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    // Ajouter la classe active au lien cliqué
    clickedLink.classList.add('active');
}

/**
 * Gestion du scroll pour mettre à jour la navigation
 */
window.addEventListener('scroll', function () {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

    let currentSection = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 150;
        const sectionHeight = section.clientHeight;

        if (window.pageYOffset >= sectionTop &&
            window.pageYOffset < sectionTop + sectionHeight) {
            currentSection = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            link.classList.add('active');
        }
    });
});

/**
 * Fonction utilitaire pour formater les nombres
 */
function formatNumber(num) {
    return new Intl.NumberFormat('fr-FR').format(num);
}

/**
 * Fonction utilitaire pour formater les pourcentages
 */
function formatPercentage(num) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'percent',
        minimumFractionDigits: 1,
        maximumFractionDigits: 1
    }).format(num);
}

/**
 * Gestion des erreurs de chargement des iframes
 */
function handleIframeErrors() {
    const iframes = document.querySelectorAll('iframe');

    iframes.forEach(iframe => {
        iframe.addEventListener('error', function () {
            const parent = this.parentElement;
            const errorDiv = document.createElement('div');
            errorDiv.className = 'alert alert-warning text-center p-4';
            errorDiv.innerHTML = `
                <i class="fas fa-exclamation-triangle me-2"></i>
                Contenu temporairement indisponible
                <br>
                <small class="text-muted">Actualisez la page ou essayez plus tard</small>
            `;
            parent.replaceChild(errorDiv, this);
        });
    });
}

// Appeler la gestion des erreurs d'iframe au chargement
handleIframeErrors();
