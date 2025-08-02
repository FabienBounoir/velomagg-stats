#!/bin/bash
# Script de mise à jour complète pour GitHub Pages
# Usage: ./update_carte.sh

echo "🗺️ Mise à jour complète VéloMAG pour GitHub Pages..."
echo "===================================================="

# Vérifier l'environnement virtuel
if [ ! -d ".venv" ]; then
    echo "❌ Environnement virtuel non trouvé"
    echo "🔧 Lancement de la configuration..."
    ./run.sh setup
fi

# Générer toutes les visualisations
echo "📡 Récupération des données en temps réel..."
.venv/bin/python interactive_viz.py

# Vérifier le succès de la génération
if [ $? -eq 0 ]; then
    echo "✅ Visualisations générées avec succès!"
    
    # Organiser les fichiers pour GitHub Pages
    echo "🗂️ Organisation des fichiers pour GitHub Pages..."
    ./organize_files.sh
    
    echo ""
    echo "✅ Mise à jour complète terminée!"
    echo "📂 Fichiers mis à jour:"
    echo "  • docs/index.html - Site principal"
    echo "  • docs/dashboard_velomagg.html - Dashboard"
    echo "  • docs/carte_velomagg.html - Carte interactive"  
    echo "  • docs/temporal_analysis.html - Analyse temporelle"
    echo "  • docs/data/ - Données CSV/JSON"
    echo "  • docs/reports/ - Rapports"
    echo ""
    echo "🚀 Pour publier les changements:"
    echo "git add docs/"
    echo "git commit -m 'Mise à jour des données VéloMAG'"
    echo "git push origin main"
    echo ""
    echo "🌐 Site accessible à:"
    echo "https://$(git config user.name 2>/dev/null || echo "VOTRE-USERNAME").github.io/$(basename $(pwd))"
    
else
    echo "❌ Erreur lors de la génération des visualisations"
    exit 1
fi
