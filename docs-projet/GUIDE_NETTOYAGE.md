# 🧹 Guide de Nettoyage - VéloMAG Stats

## Scripts de nettoyage disponibles

### 1. Nettoyage complet (`clean.py`)
```bash
python3 clean.py
```
**Supprime :**
- ✅ Tous les fichiers HTML de visualisation
- ✅ Tous les fichiers d'export (JSON, CSV, XLSX)
- ✅ Tous les répertoires temporaires (`exports/`, `reports/`, `visualizations/`, `logs/`)
- ✅ Tous les caches Python (`__pycache__/`)
- ✅ Tous les checkpoints Jupyter (`.ipynb_checkpoints/`)

**Utilisation :** Nettoyage complet avant commit Git ou réinitialisation totale

### 2. Nettoyage rapide HTML (`clean_html.py`)
```bash
python3 clean_html.py
```
**Supprime :**
- ✅ Uniquement les fichiers HTML de visualisation
- ❌ Conserve les caches et exports

**Utilisation :** Nettoyage rapide entre les générations de visualisations

### 3. Via script run.sh
```bash
./run.sh clean
```
**Fonctionnement :**
- Utilise automatiquement `clean.py` si disponible
- Sinon fait un nettoyage basique avec commandes shell

## 🔍 Fichiers supprimés par type

### Fichiers HTML générés
- `dashboard_velomagg.html` - Dashboard interactif
- `carte_velomagg.html` - Carte interactive 
- `temporal_analysis.html` - Analyse temporelle

### Fichiers d'export
- `*.json` - Statistiques et données
- `*.csv` - Exports tabulaires
- `*.xlsx` - Fichiers Excel
- `*_stats_*.json` - Rapports de statistiques
- `*_export_*.csv` - Exports de données

### Répertoires temporaires
- `exports/` - Dossier des exports
- `reports/` - Rapports générés
- `visualizations/` - Visualisations sauvegardées
- `logs/` - Fichiers de log
- `__pycache__/` - Caches Python (récursif)
- `.ipynb_checkpoints/` - Checkpoints Jupyter (récursif)

## 🚨 Problèmes fréquents

### Fichiers HTML "collés" dans les notebooks
**Symptôme :** Les visualisations HTML apparaissent en plein milieu du code
**Cause :** Fichiers HTML non supprimés entre les exécutions
**Solution :**
```bash
python3 clean_html.py  # Nettoyage rapide
# ou
python3 clean.py       # Nettoyage complet
```

### Erreurs d'espace disque
**Symptôme :** "No space left on device"
**Cause :** Accumulation de caches Python
**Solution :**
```bash
python3 clean.py  # Supprime tous les caches
```

### Fichiers de visualisation corrompus
**Symptôme :** Graphiques qui ne s'affichent pas correctement
**Cause :** Fichiers HTML partiellement écrits
**Solution :**
```bash
python3 clean_html.py  # Supprime et régénère
```

## 📋 Commandes utiles

### Vérifier la taille des caches
```bash
du -sh __pycache__ .venv/lib/python*/site-packages/__pycache__ 2>/dev/null || echo "Pas de cache trouvé"
```

### Compter les fichiers HTML
```bash
find . -name "*.html" -not -path "./venv/*" | wc -l
```

### Lister les gros fichiers
```bash
find . -size +10M -type f -not -path "./venv/*" -ls
```

## ⚙️ Configuration automatique

### Nettoyage automatique avant chaque analyse
Ajoutez dans votre `.bashrc` ou `.zshrc` :
```bash
alias velomagg-clean="cd /path/to/velomagg-stats && python3 clean_html.py"
alias velomagg-deep-clean="cd /path/to/velomagg-stats && python3 clean.py"
```

### Hook Git pre-commit
Créez `.git/hooks/pre-commit` :
```bash
#!/bin/sh
python3 clean.py
git add -A
```

## 🎯 Recommandations

1. **Avant chaque session :** `python3 clean_html.py`
2. **Après développement :** `python3 clean.py`
3. **Avant commit Git :** `./run.sh clean`
4. **En cas de problème :** Nettoyage complet + redémarrage notebook

---
*Scripts créés pour éviter l'accumulation de fichiers HTML dans les visualisations interactives*
