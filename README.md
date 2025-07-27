# Vélomagg Stats - Analyseur de données Vélomagg Montpellier

Ce projet Python permet de générer des statistiques complètes sur les stations Vélomagg de Montpellier en utilisant les APIs officielles de Montpellier Métropole.

## 🚴 Fonctionnalités

### Analyses en temps réel
- État actuel de toutes les stations
- Taux d'occupation et disponibilité
- Localisation géographique des stations
- Statistiques descriptives complètes

### Analyses temporelles
- Patterns d'utilisation par heure/jour
- Tendances d'occupation
- Identification des heures de pointe
- Analyse des variations saisonnières

### Visualisations
- Cartes de chaleur d'occupation
- Distributions statistiques
- Graphiques temporels
- Comparaisons entre stations

### Export de données
- Export CSV pour analyse externe
- Rapports JSON détaillés
- Graphiques haute résolution

## 📊 Types de statistiques générées

### Statistiques générales
- Nombre total de stations et vélos
- Taux d'occupation moyen/médian
- Capacité totale du réseau
- Stations en fonctionnement

### Analyses de distribution
- Distribution des vélos par station
- Quartiles et écarts-types
- Stations extrêmes (plus/moins occupées)
- Capacités min/max

### Patterns temporels
- Utilisation par heure de la journée
- Variations selon les jours de la semaine
- Tendances d'évolution
- Identification des pics d'usage

## 🛠 Installation

### Prérequis
- Python 3.7+
- pip

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Lancement du programme
```bash
python main.py
```

## 📈 Utilisation avancée

### Analyse temporelle personnalisée
```python
from main import VelomaggAnalyzer

analyzer = VelomaggAnalyzer()
# Analyser les 30 derniers jours d'une station
analysis = analyzer.analyze_temporal_patterns("urn:ngsi-ld:station:001", days=30)
```

### Filtrage par zone géographique
```python
# Filtrer les stations par localisation
df = analyzer.analyze_current_status()
centre_ville = df[df['locality'] == 'Montpellier']
```

## 📁 Structure des fichiers générés

```
velomagg-stats/
├── main.py                          # Programme principal
├── requirements.txt                  # Dépendances
├── velomagg_analysis.csv            # Données détaillées
├── velomagg_analysis_stats.json     # Statistiques JSON
└── visualizations/                  # Graphiques
    ├── bikes_distribution.png
    ├── occupancy_map.png
    └── top_stations.png
```

## 🔧 APIs utilisées

### API Stations
- **URL**: `https://portail-api-data.montpellier3m.fr/bikestation`
- **Description**: État actuel de toutes les stations
- **Données**: Vélos disponibles, places libres, localisation, statut

### API Séries temporelles
- **URL**: `https://portail-api-data.montpellier3m.fr/bikestation_timeseries/{station_id}/attrs/{attribute}`
- **Description**: Historique des données d'une station
- **Paramètres**: Station ID, attribut, période
- **Données**: Séries temporelles de disponibilité

## 📊 Exemples de statistiques

### Rapport général
```json
{
  "general": {
    "total_stations": 85,
    "working_stations": 82,
    "total_bikes": 450,
    "total_capacity": 850,
    "average_occupancy": 0.53
  }
}
```

### Top stations
- Station la plus occupée
- Station la moins occupée
- Plus grande/petite station
- Variations par quartier

## 🗓 Développements futurs

- [ ] Prédictions d'occupation basées sur ML
- [ ] Alertes automatiques de maintenance
- [ ] API REST pour intégration
- [ ] Dashboard web interactif
- [ ] Analyse des flux de déplacement
- [ ] Intégration données météo
- [ ] Optimisation des redistributions

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des nouvelles fonctionnalités
- Améliorer la documentation
- Optimiser le code

## 📞 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.
