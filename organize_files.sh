#!/bin/bash
# Script d'organisation des fichiers pour GitHub Pages
# Usage: ./organize_files.sh

echo "🗂️ Organisation des fichiers pour GitHub Pages..."
echo "================================================"

# Créer les répertoires nécessaires
mkdir -p docs/data docs/reports docs/visualizations

# Copier les fichiers HTML principaux
echo "📋 Copie des visualisations..."
cp dashboard_velomagg.html docs/ 2>/dev/null || echo "⚠️ dashboard_velomagg.html non trouvé"
cp carte_velomagg.html docs/ 2>/dev/null || echo "⚠️ carte_velomagg.html non trouvé"
cp temporal_analysis.html docs/ 2>/dev/null || echo "⚠️ temporal_analysis.html non trouvé"

# Copier les données
echo "📊 Copie des données..."
cp velomagg_analysis.csv docs/data/ 2>/dev/null || echo "⚠️ velomagg_analysis.csv non trouvé"
cp velomagg_analysis_stats.json docs/data/ 2>/dev/null || echo "⚠️ velomagg_analysis_stats.json non trouvé"

# Copier les rapports
echo "📄 Copie des rapports..."
cp rapport_detaille.txt docs/reports/ 2>/dev/null || echo "⚠️ rapport_detaille.txt non trouvé"

# Copier les visualisations statiques
echo "🖼️ Copie des graphiques..."
if [ -d "visualizations" ]; then
    cp -r visualizations/* docs/visualizations/ 2>/dev/null || echo "⚠️ Aucune visualisation trouvée"
else
    echo "⚠️ Dossier visualizations non trouvé"
fi

# Créer un fichier _config.yml pour GitHub Pages
echo "⚙️ Configuration GitHub Pages..."
cat > docs/_config.yml << EOF
# Configuration GitHub Pages pour VéloMAG Stats
title: "VéloMAG Stats"
description: "Analyse en temps réel du système de vélos en libre-service de Montpellier"
baseurl: ""
url: "https://$(git config user.name).github.io"

# Jekyll configuration
markdown: kramdown
highlighter: rouge
theme: null

# Exclude files
exclude:
  - README.md
  - LICENSE
  - "*.py"
  - "*.sh"
  - ".venv/"
  - "__pycache__/"

# Include files
include:
  - assets/
  - data/
  - reports/
  - visualizations/

# Plugins
plugins:
  - jekyll-sitemap
  - jekyll-feed

# SEO
lang: fr
author: VéloMAG Analytics
EOF

# Créer un README pour le dossier docs
cat > docs/README.md << EOF
# VéloMAG Stats - GitHub Pages

Ce dossier contient les fichiers pour le site web GitHub Pages.

## Structure

- \`index.html\` - Page principale du site
- \`assets/\` - CSS, JS et autres ressources
- \`data/\` - Fichiers de données (CSV, JSON)
- \`reports/\` - Rapports texte
- \`visualizations/\` - Graphiques statiques

## Mise à jour

Pour mettre à jour les données du site, exécutez :

\`\`\`bash
./organize_files.sh
\`\`\`

## Configuration GitHub Pages

1. Aller dans Settings > Pages
2. Source: Deploy from a branch
3. Branch: main
4. Folder: /docs
EOF

# Créer un .gitignore pour le dossier docs
cat > docs/.gitignore << EOF
# Fichiers temporaires
*.tmp
*.temp
.DS_Store

# Logs
*.log
EOF

# Créer un index.json pour l'API des données
echo "🔧 Création de l'index API..."
cat > docs/data/index.json << EOF
{
  "api": {
    "version": "1.0",
    "last_update": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "endpoints": {
      "csv": "velomagg_analysis.csv",
      "json": "velomagg_analysis_stats.json",
      "reports": "../reports/rapport_detaille.txt",
      "visualizations": "../visualizations/"
    }
  },
  "description": "API des données VéloMAG Stats"
}
EOF

# Afficher la structure finale
echo ""
echo "✅ Organisation terminée!"
echo ""
echo "📁 Structure créée:"
echo "docs/"
echo "├── index.html (page principale)"
echo "├── dashboard_velomagg.html"
echo "├── carte_velomagg.html"
echo "├── temporal_analysis.html"
echo "├── assets/"
echo "│   ├── css/style.css"
echo "│   └── js/app.js"
echo "├── data/"
echo "│   ├── velomagg_analysis.csv"
echo "│   ├── velomagg_analysis_stats.json"
echo "│   └── index.json"
echo "├── reports/"
echo "│   └── rapport_detaille.txt"
echo "└── visualizations/"
echo "    └── (graphiques PNG)"
echo ""
echo "🚀 Pour activer GitHub Pages:"
echo "1. Aller dans Settings > Pages de votre repo GitHub"
echo "2. Source: Deploy from a branch"  
echo "3. Branch: main"
echo "4. Folder: /docs"
echo ""
echo "🌐 Votre site sera disponible à:"
echo "https://$(git config user.name 2>/dev/null || echo "USERNAME").github.io/$(basename $(pwd))"
