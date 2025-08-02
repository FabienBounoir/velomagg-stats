# Guide d'utilisation - VéloMAG Stats

## 🎯 Vue d'ensemble

Ce projet Python complet permet d'analyser en profondeur les données du système de vélos en libre-service VéloMAG de Montpellier. Il utilise les APIs officielles de Montpellier Métropole pour générer des statistiques détaillées, des visualisations interactives et des rapports automatisés.

## 🚀 Démarrage rapide

### 1. Configuration initiale
```bash
./run.sh setup
```

### 2. Lancement de l'analyse
```bash
# Analyse standard
./run.sh analyze

# Analyse avancée avec recommandations
./run.sh advanced
```

### 3. Notebook interactif
Ouvrez `velomagg_analysis.ipynb` dans VS Code et exécutez les cellules une par une pour une analyse interactive.

## 📊 Types d'analyses disponibles

### Analyse standard (`main.py`)
- État actuel de toutes les stations
- Statistiques descriptives
- Visualisations de base
- Export CSV/JSON
- Analyse temporelle d'exemple

**Fichiers générés :**
- `velomagg_analysis.csv` : Données détaillées
- `velomagg_analysis_stats.json` : Statistiques JSON
- `visualizations/` : Graphiques PNG

### Analyse avancée (`advanced_analytics.py`)
- Calcul des scores d'efficacité
- Identification des stations problématiques
- Analyse de couverture géographique
- Recommandations d'optimisation
- Rapport exécutif détaillé

**Fichiers générés :**
- `rapport_detaille.txt` : Rapport complet
- Toutes les analyses de l'analyse standard

### Notebook interactif (`velomagg_analysis.ipynb`)
- Analyse étape par étape
- Visualisations interactives avec Plotly
- Cartes interactives avec Folium
- Clustering géographique
- Dashboard complet

## 🔧 Configuration technique

### Environnement Python
- Python 3.13+ (environnement virtuel automatique)
- Dépendances installées automatiquement

### APIs utilisées
1. **API Stations** : État en temps réel
   - URL : `https://portail-api-data.montpellier3m.fr/bikestation`
   - Données : Position, capacité, vélos disponibles

2. **API Séries temporelles** : Données historiques
   - URL : `https://portail-api-data.montpellier3m.fr/bikestation_timeseries/{station_id}/attrs/{attribute}`
   - Données : Évolution temporelle par station

## 📈 Métriques calculées

### Métriques de base
- **Taux d'occupation** : `vélos_disponibles / capacité_totale`
- **Taux d'utilisation** : `places_occupées / capacité_totale`
- **Disponibilité** : Statut opérationnel des stations

### Métriques avancées
- **Score d'efficacité** : Combinaison pondérée de :
  - Score d'équilibre (optimal à 50%)
  - Score de disponibilité (évite vide/plein)
  - Score d'utilisation
- **Clusters géographiques** : Regroupement par K-means
- **Patterns temporels** : Tendances horaires/quotidiennes

## 🗺️ Analyses géographiques

### Cartes interactives
- Localisation de toutes les stations
- Couleurs basées sur le taux d'occupation
- Taille des marqueurs = capacité
- Popups informatifs détaillés

### Clustering spatial
- Identification de zones géographiques
- Analyse des performances par cluster
- Calcul des distances entre stations
- Détection des zones sous-desservies

## ⏰ Analyses temporelles

### Patterns d'usage
- Variations horaires
- Différences week-end/semaine
- Identification des heures de pointe
- Tendances saisonnières (si données disponibles)

### Prédictions
- Heures de pointe prédites
- Patterns de demande
- Analyse du turnover des vélos

## 📊 Visualisations disponibles

### Graphiques statiques (Matplotlib/Seaborn)
- Histogrammes de distribution
- Cartes de chaleur d'occupation
- Boxplots comparatifs
- Scatter plots de corrélation

### Visualisations interactives (Plotly)
- Dashboard multi-métriques
- Graphiques temporels avec zoom
- Matrices de corrélation interactives
- Graphiques radar par cluster

### Cartes (Folium)
- Carte principale avec toutes les stations
- Légendes et contrôles de couches
- Cartes de densité
- Visualisation des clusters

## 📋 Formats d'export

### Données structurées
- **CSV** : Compatible Excel, analyse externe
- **JSON** : APIs, intégration système
- **Excel** : Rapports business

### Rapports
- **Markdown** : Documentation, GitHub
- **TXT** : Rapports exécutifs
- **HTML** : Visualisations web

## 🚨 Alertes et monitoring

### Stations problématiques détectées
- **Stations vides** : 0 vélos disponibles
- **Stations pleines** : 0 places libres
- **Stations hors service** : Status ≠ "working"
- **Faible efficacité** : Score < 30%

### Recommandations automatiques
- Redistribution urgente
- Maintenance préventive
- Ajustement des capacités
- Optimisation du réseau

## 🔍 Cas d'usage

### Gestionnaires du réseau VéloMAG
- Monitoring temps réel
- Optimisation des redistributions
- Planification de maintenance
- Analyse de performance

### Analystes de données
- Recherche de patterns
- Modélisation prédictive
- Analyse comportementale
- Études d'impact

### Développeurs
- Intégration API
- Dashboard personnalisés
- Applications mobiles
- Systèmes d'alertes

## 🛠️ Personnalisation

### Modification des seuils
```python
# Dans main.py ou advanced_analytics.py
EFFICIENCY_THRESHOLD = 0.3  # Seuil efficacité
OCCUPANCY_OPTIMAL_MIN = 0.4  # Taux optimal min
OCCUPANCY_OPTIMAL_MAX = 0.6  # Taux optimal max
```

### Ajout de nouvelles métriques
```python
def custom_metric(df):
    # Votre calcul personnalisé
    df['custom_score'] = your_formula
    return df
```

### Nouvelles visualisations
```python
# Ajouter dans la section visualisations
fig, ax = plt.subplots()
# Votre graphique personnalisé
```

## 📞 Support et contribution

### Problèmes fréquents
1. **Erreur API** : Vérifier la connectivité Internet
2. **Données manquantes** : APIs parfois indisponibles
3. **Performance** : Limiter le nombre de stations analysées

### Améliorations suggérées
- Prédictions machine learning
- Alertes en temps réel
- Dashboard web
- Intégration données météo
- Analyse des flux de mobilité

### Contact
- Ouvrir une issue sur GitHub
- Consulter la documentation API officielle
- Vérifier les logs dans `logs/`

---

*Documentation générée automatiquement - VéloMAG Stats v1.0*
