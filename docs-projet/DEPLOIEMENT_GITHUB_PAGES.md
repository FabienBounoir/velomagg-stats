# 🚀 Guide de Déploiement GitHub Pages

## Étapes pour publier votre site VéloMAG

### 1. Initialisation (première fois seulement)

```bash
# Rendre les scripts exécutables
chmod +x *.sh

# Générer les visualisations
./update_carte.sh

# Initialiser GitHub Pages
./init-github-pages.sh
```

### 2. Configuration GitHub (dans votre navigateur)

1. Aller sur **GitHub.com** > votre repository
2. **Settings** > **Pages**
3. **Source** : Deploy from a branch
4. **Branch** : main
5. **Folder** : /docs
6. Cliquer **Save**

### 3. URL de votre site

Votre site sera disponible à :
```
https://VOTRE-USERNAME.github.io/velomagg-stats
```

### 4. Mises à jour automatiques

Le site se met à jour automatiquement :
- **Toutes les 4 heures** (via GitHub Actions)
- **À chaque push** sur la branche main
- **Manuellement** en cliquant "Run workflow" dans Actions

### 5. Mise à jour manuelle

```bash
# Générer nouvelles données et organiser
./update_carte.sh

# Publier sur GitHub
git add docs/
git commit -m "Mise à jour données $(date)"
git push origin main
```

## 📊 Structure du Site

- **Page d'accueil** : Vue d'ensemble avec statistiques
- **Carte interactive** : Visualisation géographique des 20 stations
- **Dashboard** : Analyses détaillées et graphiques
- **Analyse temporelle** : Évolution dans le temps

## 🔧 Maintenance

### Ajouter de nouvelles visualisations
1. Modifier `interactive_viz.py`
2. Tester avec `./update_carte.sh`
3. Commit et push

### Personnaliser le design
1. Modifier `docs/assets/css/style.css`
2. Modifier `docs/assets/js/app.js`
3. Commit et push

### Vérifier les logs
- GitHub Actions : onglet "Actions" de votre repository
- Logs d'erreur : voir la sortie des scripts

## 🆘 Dépannage

**Site pas accessible ?**
- Vérifier que GitHub Pages est activé
- Attendre 5-10 minutes après activation
- Vérifier l'onglet Actions pour erreurs

**Données pas à jour ?**
- Relancer `./update_carte.sh`
- Vérifier la connexion internet
- Consulter les logs dans GitHub Actions

**Erreur 404 ?**
- Vérifier que `/docs` est sélectionné comme dossier source
- S'assurer que `docs/index.html` existe

---

💡 **Pour toute question, consulter la documentation GitHub Pages officielle**
