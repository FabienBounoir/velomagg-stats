# VéloMAG Stats - GitHub Pages

🚴‍♂️ **Site web de visualisation des données VéloMAG de Montpellier Métropole**

## 📊 Contenu du Site

### Pages Principales
- **Accueil** (`index.html`) - Dashboard principal avec aperçu global
- **Carte Interactive** (`carte_velomagg.html`) - Visualisation géographique des 20 stations
- **Dashboard Complet** (`dashboard_velomagg.html`) - Analyses détaillées
- **Analyse Temporelle** (`temporal_analysis.html`) - Évolution dans le temps

### Données
- **Temps réel** : Données actualisées depuis l'API officielle
- **Historique** : Analyses des tendances d'utilisation
- **Géolocalisation** : Positions exactes des stations
- **Occupation** : Taux d'utilisation par station

## 🔧 Structure Technique

```
docs/
├── index.html                    # Page d'accueil
├── carte_velomagg.html          # Carte interactive
├── dashboard_velomagg.html      # Dashboard
├── temporal_analysis.html       # Analyse temporelle
├── assets/
│   ├── css/style.css           # Styles personnalisés
│   └── js/app.js               # JavaScript
├── data/
│   ├── velomagg_analysis.csv   # Données CSV
│   └── velomagg_analysis_stats.json
└── reports/
    └── rapport_detaille.txt     # Rapport détaillé
```

## 🚀 Technologies Utilisées

- **Frontend** : HTML5, CSS3, JavaScript ES6
- **Framework** : Bootstrap 5.3.0
- **Cartographie** : Leaflet.js + OpenStreetMap
- **Visualisations** : Chart.js, Plotly.js
- **Icônes** : Font Awesome 6
- **Hébergement** : GitHub Pages

## 📈 Données VéloMAG

Les données proviennent de l'API officielle de Montpellier Métropole :
- **API** : `https://portail-api-data.montpellier3m.fr/bikestation`
- **Stations** : 20 stations actives dans Montpellier
- **Mise à jour** : Temps réel

### Informations Disponibles
- Position GPS de chaque station
- Nombre de vélos disponibles
- Nombre d'emplacements libres
- État opérationnel
- Tendances d'utilisation

## 🔄 Mise à Jour

Pour mettre à jour les données du site, exécutez depuis le répertoire racine :

```bash
./update_carte.sh
```

## ⚙️ Configuration GitHub Pages

1. Aller dans **Settings > Pages**
2. Source: **Deploy from a branch**
3. Branch: **main**
4. Folder: **/docs**

---

💡 **Projet développé avec l'API ouverte de Montpellier Métropole**
