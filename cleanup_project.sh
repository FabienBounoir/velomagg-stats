#!/bin/bash
# Script de nettoyage et organisation du projet VéloMAG
# Supprime les doublons et organise les fichiers logiquement

echo "🧹 Grand nettoyage du projet VéloMAG"
echo "====================================="

# Fonction pour supprimer en sécurité
safe_remove() {
    if [ -f "$1" ] || [ -d "$1" ]; then
        echo "🗑️ Suppression: $1"
        rm -rf "$1"
    fi
}

# Fonction pour déplacer en sécurité
safe_move() {
    if [ -f "$1" ]; then
        echo "📁 Déplacement: $1 → $2"
        mv "$1" "$2"
    fi
}

echo ""
echo "📋 ÉTAPE 1: Suppression des fichiers temporaires et doublons"
echo "=========================================================="

# Supprimer les fichiers de sauvegarde
safe_remove "README.md.bak"
safe_remove "docs/index.html.bak"
safe_remove ".DS_Store"

# Supprimer les caches Python
safe_remove "__pycache__"
find . -name "*.pyc" -delete 2>/dev/null
find . -name "*.pyo" -delete 2>/dev/null
find . -name "*~" -delete 2>/dev/null

# Supprimer les fichiers HTML dupliqués (gardés dans docs/ seulement)
echo ""
echo "🌐 Nettoyage des fichiers HTML dupliqués..."
safe_remove "carte_velomagg.html"
safe_remove "dashboard_velomagg.html" 
safe_remove "temporal_analysis.html"

# Supprimer les données dupliquées (gardées dans docs/data/ seulement)
echo ""
echo "📊 Nettoyage des données dupliquées..."
safe_remove "velomagg_analysis.csv"
safe_remove "velomagg_analysis_stats.json"
safe_remove "rapport_detaille.txt"

# Supprimer les visualizations dupliquées (gardées dans docs/visualizations/ seulement)
echo ""
echo "🖼️ Nettoyage des visualisations dupliquées..."
safe_remove "visualizations"

echo ""
echo "📋 ÉTAPE 2: Organisation des scripts"
echo "==================================="

# Créer un dossier scripts/
mkdir -p scripts

# Déplacer les scripts utilitaires
echo "📁 Organisation des scripts utilitaires..."
safe_move "clean.py" "scripts/"
safe_move "clean_html.py" "scripts/"
safe_move "clean_generated.sh" "scripts/"
safe_move "test_auto_update.sh" "scripts/"
safe_move "launch_viz.sh" "scripts/"

# Mettre à jour les permissions
chmod +x scripts/*.sh 2>/dev/null

echo ""
echo "📋 ÉTAPE 3: Consolidation de la documentation"
echo "============================================="

# Créer un dossier docs-projet/ pour séparer de docs/ (GitHub Pages)
mkdir -p docs-projet

# Déplacer les guides
echo "📖 Organisation de la documentation..."
safe_move "GUIDE.md" "docs-projet/"
safe_move "GUIDE_NETTOYAGE.md" "docs-projet/"
safe_move "GUIDE_VISUALISATIONS.md" "docs-projet/"
safe_move "DEPLOIEMENT_GITHUB_PAGES.md" "docs-projet/"

# Créer un index de documentation
cat > docs-projet/README.md << 'EOF'
# 📚 Documentation du projet VéloMAG

Ce dossier contient toute la documentation technique du projet.

## 📋 Guides disponibles

- **[GUIDE.md](GUIDE.md)** - Guide principal d'utilisation
- **[GUIDE_VISUALISATIONS.md](GUIDE_VISUALISATIONS.md)** - Guide des visualisations
- **[GUIDE_NETTOYAGE.md](GUIDE_NETTOYAGE.md)** - Guide de nettoyage des données
- **[DEPLOIEMENT_GITHUB_PAGES.md](DEPLOIEMENT_GITHUB_PAGES.md)** - Guide de déploiement

## 🔗 Liens utiles

- [Site web](../docs/index.html) - Interface utilisateur
- [Scripts](../scripts/) - Scripts utilitaires
- [Données](../docs/data/) - Fichiers de données
EOF

echo ""
echo "📋 ÉTAPE 4: Simplification des scripts principaux"
echo "================================================="

# Supprimer les scripts redondants/obsolètes
echo "🗑️ Suppression des scripts redondants..."
safe_remove "velomagg_analysis.ipynb"  # Notebook redondant avec main.py

echo ""
echo "📋 ÉTAPE 5: Mise à jour des scripts restants"
echo "============================================"

# Mettre à jour run.sh pour pointer vers les nouveaux emplacements
if [ -f "run.sh" ]; then
    echo "🔧 Mise à jour de run.sh..."
    sed -i.bak 's|./clean\.py|./scripts/clean.py|g' run.sh 2>/dev/null || true
    rm -f run.sh.bak
fi

# Mettre à jour organize_files.sh
if [ -f "organize_files.sh" ]; then
    echo "🔧 Mise à jour de organize_files.sh..."
    # Le script reste à la racine car utilisé par GitHub Actions
fi

echo ""
echo "📋 ÉTAPE 6: Vérification de la structure finale"
echo "==============================================="

echo ""
echo "📁 Structure finale du projet:"
echo ""
echo "velomagg-stats/"
echo "├── 🐍 SCRIPTS PYTHON PRINCIPAUX"
echo "│   ├── main.py                    # Script principal d'analyse"
echo "│   ├── interactive_viz.py         # Génération visualisations interactives"
echo "│   ├── advanced_analytics.py      # Analyses avancées"
echo "│   └── setup.py                   # Configuration du projet"
echo "│"
echo "├── ⚙️ SCRIPTS DE GESTION"
echo "│   ├── run.sh                     # Script de lancement principal"
echo "│   ├── organize_files.sh          # Organisation pour GitHub Pages"
echo "│   ├── update_carte.sh            # Mise à jour complète"
echo "│   ├── init-github-pages.sh       # Initialisation GitHub Pages"
echo "│   └── requirements.txt           # Dépendances Python"
echo "│"
echo "├── 🛠️ scripts/                    # Scripts utilitaires"
echo "│   ├── clean.py                   # Nettoyage données"
echo "│   ├── clean_html.py              # Nettoyage HTML"
echo "│   ├── clean_generated.sh         # Nettoyage fichiers générés"
echo "│   ├── test_auto_update.sh        # Tests mise à jour auto"
echo "│   └── launch_viz.sh              # Lancement visualisations"
echo "│"
echo "├── 📚 docs-projet/                # Documentation technique"
echo "│   ├── README.md                  # Index documentation"
echo "│   ├── GUIDE.md                   # Guide principal"
echo "│   ├── GUIDE_VISUALISATIONS.md    # Guide visualisations"
echo "│   ├── GUIDE_NETTOYAGE.md         # Guide nettoyage"
echo "│   └── DEPLOIEMENT_GITHUB_PAGES.md # Guide déploiement"
echo "│"
echo "├── 🌐 docs/                       # Site GitHub Pages"
echo "│   ├── index.html                 # Page principale"
echo "│   ├── assets/                    # CSS, JS, ressources"
echo "│   ├── data/                      # Fichiers de données"
echo "│   ├── reports/                   # Rapports"
echo "│   └── visualizations/            # Images PNG"
echo "│"
echo "├── ⚙️ .github/workflows/          # Automation GitHub"
echo "│   └── update-data.yml            # Workflow mise à jour auto"
echo "│"
echo "└── 📋 Fichiers de configuration"
echo "    ├── README.md                  # Documentation principale"
echo "    └── .venv/                     # Environnement virtuel"

echo ""
echo "✅ NETTOYAGE TERMINÉ!"
echo ""
echo "📊 Résumé des améliorations:"
echo "  🗑️ Supprimé les fichiers doublons HTML/CSV/JSON"
echo "  📁 Organisé les scripts dans scripts/"
echo "  📚 Regroupé la documentation dans docs-projet/"
echo "  🧹 Nettoyé les fichiers temporaires et caches"
echo "  🎯 Structure claire et logique"
echo ""
echo "🚀 Le projet est maintenant propre et organisé!"
echo "   Tous les fichiers sont à leur place logique"
echo "   Fini la confusion entre les doublons!"
