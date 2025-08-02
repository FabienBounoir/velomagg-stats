#!/bin/bash

# Script de mise à jour des statistiques dans le README
echo "📊 Mise à jour du README avec les statistiques actuelles..."

# Vérifier si le fichier JSON existe
if [ ! -f "docs/data/velomagg_analysis_stats.json" ]; then
    echo "❌ Fichier de statistiques non trouvé!"
    exit 1
fi

# Vérifier si jq est installé
if ! command -v jq &> /dev/null; then
    echo "⚠️ Installation de jq..."
    brew install jq || (echo "❌ Impossible d'installer jq" && exit 1)
fi

# Vérifier si bc est installé
if ! command -v bc &> /dev/null; then
    echo "⚠️ Installation de bc..."
    brew install bc || (echo "❌ Impossible d'installer bc" && exit 1)
fi

# Extraire les statistiques du JSON
STATS_FILE="docs/data/velomagg_analysis_stats.json"
TOTAL_STATIONS=$(jq -r '.general.total_stations' "$STATS_FILE")
TOTAL_BIKES=$(jq -r '.general.total_bikes' "$STATS_FILE")
TOTAL_CAPACITY=$(jq -r '.general.total_capacity' "$STATS_FILE")
AVERAGE_OCCUPANCY=$(jq -r '.general.average_occupancy' "$STATS_FILE")
BEST_STATION=$(jq -r '.extremes.most_occupied.address' "$STATS_FILE")
BEST_RATE=$(jq -r '.extremes.most_occupied.occupancy_rate' "$STATS_FILE")
WORST_STATION=$(jq -r '.extremes.least_occupied.address' "$STATS_FILE")
WORST_RATE=$(jq -r '.extremes.least_occupied.occupancy_rate' "$STATS_FILE")

# Convertir le taux d'occupation en pourcentage
OCCUPANCY_PERCENT=$(echo "$AVERAGE_OCCUPANCY * 100" | bc -l | cut -d. -f1)

# Date de dernière mise à jour
LAST_UPDATE=$(date '+%d/%m/%Y à %H:%M')

# Créer le nouveau README
cat > README.md << EOF
# 🚴 VéloMAG Analytics - Montpellier

[![Mise à jour automatique](https://github.com/FabienBounoir/velomagg-stats/actions/workflows/update-data.yml/badge.svg)](https://github.com/FabienBounoir/velomagg-stats/actions/workflows/update-data.yml)

## 📊 Statistiques en temps réel

**Dernière mise à jour :** $LAST_UPDATE

| Métrique | Valeur |
|----------|--------|
| 🏢 **Stations totales** | $TOTAL_STATIONS |
| 🚴 **Vélos disponibles** | $TOTAL_BIKES |
| 📍 **Capacité totale** | $TOTAL_CAPACITY places |
| 📊 **Taux d'occupation** | $OCCUPANCY_PERCENT% |

### 🏆 Performances des stations

- **Station la plus fréquentée :** $BEST_STATION ($(echo "$BEST_RATE * 100" | bc -l | cut -d. -f1)%)
- **Station la moins fréquentée :** $WORST_STATION ($(echo "$WORST_RATE * 100" | bc -l | cut -d. -f1)%)

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

\`\`\`bash
# Cloner le projet
git clone https://github.com/FabienBounoir/velomagg-stats.git
cd velomagg-stats

# Installer les dépendances
pip install -r requirements.txt
\`\`\`

### Génération des analyses

\`\`\`bash
# Analyse complète
python main.py

# Visualisations interactives 
python interactive_viz.py

# Analyses avancées
python advanced_analytics.py

# Mise à jour pour GitHub Pages
./update_carte.sh
\`\`\`

## 📁 Structure du projet

\`\`\`
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
\`\`\`

## 🔄 Automatisation

Les données sont automatiquement mises à jour **2 fois par jour** (8h et 20h UTC) via GitHub Actions.

## 📡 Source des données

- **API VéloMAG :** [Portail Open Data Montpellier](https://portail-api-data.montpellier3m.fr/bikestation)
- **Fréquence :** Temps réel
- **Couverture :** $TOTAL_STATIONS stations actives

## 🛠️ Technologies

- **Python** : Pandas, Matplotlib, Seaborn, Plotly, Folium
- **Web** : HTML5, Bootstrap 5, JavaScript
- **Déploiement** : GitHub Pages, GitHub Actions
- **Données** : API REST, JSON, CSV

---

⭐ **N'hésitez pas à mettre une étoile si ce projet vous intéresse !**
EOF

echo "✅ README mis à jour avec les statistiques actuelles :"
echo "   📊 $TOTAL_STATIONS stations, $TOTAL_BIKES vélos, $OCCUPANCY_PERCENT% d'occupation"
echo "   🏆 Meilleure: $BEST_STATION ($(echo "$BEST_RATE * 100" | bc -l | cut -d. -f1)%)"
echo "   📉 Moins occupée: $WORST_STATION ($(echo "$WORST_RATE * 100" | bc -l | cut -d. -f1)%)"
