#!/usr/bin/env bash

# Script de lancement rapide pour VéloMAG Stats
# Usage: ./run.sh [command]

set -e

VENV_PATH="/Users/fabienbounoir/Documents/project/velomagg-stats/.venv/bin/python"

echo "🚴 VéloMAG Stats - Script de lancement"
echo "======================================"

case "${1:-help}" in
    "setup")
        echo "🔧 Configuration du projet..."
        $VENV_PATH setup.py
        ;;
    "analyze")
        echo "📊 Lancement de l'analyse principale..."
        $VENV_PATH main.py
        ;;
    "advanced")
        echo "🔬 Lancement de l'analyse avancée..."
        $VENV_PATH advanced_analytics.py
        ;;
    "notebook")
        echo "📓 Ouverture du notebook Jupyter..."
        echo "Utilisez VS Code pour ouvrir: velomagg_analysis.ipynb"
        ;;
    "clean")
        echo "🧹 Nettoyage des fichiers générés..."
        if [ -f "clean.py" ]; then
            echo "🔧 Utilisation du script de nettoyage avancé..."
            python3 clean.py
        else
            echo "📁 Nettoyage basique..."
            rm -rf exports/ reports/ visualizations/ logs/
            rm -f *.html *.json *.csv *.xlsx
            echo "🗑️  Suppression des fichiers HTML et exports"
            find . -name "*.html" -not -path "./venv/*" -delete 2>/dev/null || true
            find . -name "*_stats_*.json" -delete 2>/dev/null || true
            find . -name "*_export_*.csv" -delete 2>/dev/null || true
            find . -name "*_export_*.xlsx" -delete 2>/dev/null || true
            echo "✅ Nettoyage terminé"
        fi
        ;;
    "install")
        echo "📦 Installation des dépendances..."
        $VENV_PATH -m pip install -r requirements.txt
        ;;
    *)
        echo "📋 Commandes disponibles:"
        echo "  ./run.sh setup     - Configuration initiale"
        echo "  ./run.sh analyze   - Analyse standard"
        echo "  ./run.sh advanced  - Analyse avancée"
        echo "  ./run.sh notebook  - Notebook Jupyter"
        echo "  ./run.sh install   - Installer dépendances"
        echo "  ./run.sh clean     - Nettoyer fichiers"
        echo ""
        echo "📁 Structure du projet:"
        echo "  main.py                    - Programme principal"
        echo "  advanced_analytics.py      - Analyses avancées"
        echo "  velomagg_analysis.ipynb    - Notebook interactif"
        echo "  setup.py                   - Configuration"
        echo "  requirements.txt           - Dépendances"
        ;;
esac
