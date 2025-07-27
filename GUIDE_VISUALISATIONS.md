# 🎨 Guide des Visualisations Interactives VéloMAG

## 🚀 Lancement rapide

### **Méthode 1: Script automatisé (Recommandé)**
```bash
# Toutes les visualisations
./launch_viz.sh

# Spécifiques
./launch_viz.sh dashboard    # Dashboard Plotly uniquement
./launch_viz.sh map         # Carte interactive uniquement  
./launch_viz.sh notebook    # Jupyter Notebook
```

### **Méthode 2: Script Python direct**
```bash
# Avec l'environnement virtuel
.venv/bin/python interactive_viz.py

# Autres analyses
.venv/bin/python advanced_analytics.py
.venv/bin/python main.py
```

### **Méthode 3: Notebook Jupyter**
```bash
# Dans VS Code (recommandé)
code velomagg_analysis.ipynb

# Ou en ligne de commande
jupyter notebook velomagg_analysis.ipynb
```

## 📊 Visualisations disponibles

### **1. Dashboard Plotly interactif** 
- **Fichier**: `dashboard_velomagg.html`
- **Contenu**: 4 graphiques en tableau de bord
  - Histogramme des vélos disponibles
  - Scatter plot taux d'occupation vs capacité
  - Box plot des scores d'efficacité
  - Camembert des statuts de stations
- **Interactions**: Zoom, hover, filtres, sélection

### **2. Carte interactive Folium**
- **Fichier**: `carte_velomagg.html`
- **Contenu**: Carte géographique de Montpellier
  - Markers colorés par taux d'occupation
  - Pop-ups avec détails des stations
  - Heatmap de densité d'utilisation
  - Contrôles de couches
- **Navigation**: Zoom, déplacement, clic sur stations

### **3. Analyse temporelle**
- **Fichier**: `temporal_analysis.html`
- **Contenu**: Courbes d'évolution temporelle
  - Patterns d'usage horaire
  - Comparaison multi-stations
  - Prédictions de pics d'usage
- **Interactions**: Légendes cliquables, zoom temporel

### **4. Notebook Jupyter complet**
- **Fichier**: `velomagg_analysis.ipynb`
- **Contenu**: Toutes les analyses dans un seul fichier
  - 9 sections complètes d'analyses
  - Visualisations interactives intégrées
  - Exports automatiques
  - Clustering géographique

## ⚡ Tests et vérifications

### **Vérifier que tout fonctionne:**
```bash
# Test rapide
.venv/bin/python -c "
from interactive_viz import InteractiveVisualizer
viz = InteractiveVisualizer()
print('✅ Modules importés avec succès')
df = viz.analyzer.analyze_current_status()
print(f'✅ {len(df)} stations récupérées')
"
```

### **Fichiers générés:**
Après exécution, vous devriez avoir :
- ✅ `dashboard_velomagg.html` (Dashboard principal)
- ✅ `carte_velomagg.html` (Carte interactive)
- ✅ `temporal_analysis.html` (Analyse temporelle)
- ✅ `rapport_detaille.txt` (Rapport textuel)

## 🛠️ Résolution de problèmes

### **Erreur "Module not found":**
```bash
# Réinstaller les dépendances
.venv/bin/pip install plotly folium pandas requests
```

### **Erreur d'API:**
```bash
# Vérifier la connectivité
.venv/bin/python -c "
import requests
r = requests.get('https://data.montpellier3m.fr/api/records/1.0/search/?dataset=bikestation')
print(f'Status: {r.status_code}')
"
```

### **Problème d'affichage:**
- Les fichiers HTML sont autonomes et s'ouvrent dans n'importe quel navigateur
- Double-cliquer sur les fichiers `.html` pour les ouvrir
- Ou utiliser : `open dashboard_velomagg.html` (macOS)

## 📱 Utilisation avancée

### **Personnaliser les visualisations:**
Modifiez `interactive_viz.py` pour :
- Changer les couleurs : `colors = ['blue', 'red', 'green']`
- Ajuster le nombre de stations : `sample_size=10`
- Modifier la période d'analyse : `days=30`

### **Exporter vers d'autres formats:**
```python
# Dans le script Python
fig.write_image("dashboard.png")  # PNG
fig.write_image("dashboard.pdf")  # PDF
```

### **Automatiser les mises à jour:**
```bash
# Crontab pour mise à jour automatique
# 0 */2 * * * cd /path/to/project && .venv/bin/python interactive_viz.py
```

## 🎯 Types de visualisations par usage

| **Besoin** | **Fichier recommandé** |
|------------|------------------------|
| **Présentation** | `dashboard_velomagg.html` |
| **Exploration géographique** | `carte_velomagg.html` |
| **Analyse temporelle** | `temporal_analysis.html` |
| **Recherche approfondie** | `velomagg_analysis.ipynb` |
| **Rapport exécutif** | `.venv/bin/python advanced_analytics.py` |

---

🎉 **Toutes les visualisations sont mises à jour automatiquement avec les données temps réel des APIs de Montpellier !** 🚴‍♀️
