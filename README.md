# 🚴 VéloMAG Analytics - Montpellier

[![Mise à jour automatique](https://github.com/FabienBounoir/velomagg-stats/actions/workflows/update-data.yml/badge.svg)](https://github.com/FabienBounoir/velomagg-stats/actions/workflows/update-data.yml)

## 📊 Statistiques en temps réel

**Dernière mise à jour :** 06/02/2026 à 08:41

| Métrique | Valeur |
|----------|--------|
| 🏢 **Stations totales** | 20 |
| 🚴 **Vélos disponibles** | 100 |
| 📍 **Capacité totale** | 271 places |
| 📊 **Taux d'occupation** | 37% |

### 🏆 Performances des stations

- **Station la plus fréquentée :** Les Aubes (87%)
- **Station la moins fréquentée :** Rue Jules Ferry - Gare Saint-Roch (0%)

## 🌐 Site Web Interactif

**👉 [Accéder au site VéloMAG Analytics](https://fabienbounoir.github.io/velomagg-stats/)**

### 📋 Fonctionnalités disponibles

- 🗺️ **Carte interactive** - Localisation et état en temps réel des stations
- 📊 **Dashboard complet** - Graphiques et statistiques détaillées  
- ⏰ **Analyse temporelle** - Évolution des données dans le temps
- 📈 **Visualisations** - Graphiques PNG téléchargeables
- 📄 **Rapports** - Analyses détaillées au format texte

## 🚀 Utilisation locale

### Installation

```bash
# Cloner le projet
git clone https://github.com/FabienBounoir/velomagg-stats.git
cd velomagg-stats

# Installer les dépendances
pip install -r requirements.txt
```

### Génération des analyses

```bash
# Analyse complète
python main.py

# Visualisations interactives 
python interactive_viz.py

# Analyses avancées
python advanced_analytics.py

# Mise à jour pour GitHub Pages
./update_carte.sh
```

## 📁 Structure du projet

```
velomagg-stats/
├── docs/                    # Site GitHub Pages
│   ├── index.html          # Page d'accueil
│   ├── dashboard_velomagg.html
│   ├── carte_velomagg.html
│   ├── temporal_analysis.html
│   ├── data/               # Données JSON/CSV
│   ├── visualizations/     # Graphiques PNG
│   └── reports/           # Rapports détaillés
├── scripts/               # Scripts d'automatisation
├── docs-projet/          # Documentation technique
└── exports/              # Données historiques
```

## 🔄 Automatisation

Les données sont automatiquement mises à jour **2 fois par jour** (8h et 20h UTC) via GitHub Actions.

## 📡 Source des données

- **API VéloMAG :** [Portail Open Data Montpellier](https://portail-api-data.montpellier3m.fr/bikestation)
- **Fréquence :** Temps réel
- **Couverture :** 20 stations actives

## 🛠️ Technologies

- **Python** : Pandas, Matplotlib, Seaborn, Plotly, Folium
- **Web** : HTML5, Bootstrap 5, JavaScript
- **Déploiement** : GitHub Pages, GitHub Actions
- **Données** : API REST, JSON, CSV

---

⭐ **N'hésitez pas à mettre une étoile si ce projet vous intéresse !**
