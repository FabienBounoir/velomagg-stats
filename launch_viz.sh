#!/bin/bash

# 🎨 Script de lancement des visualisations interactives VéloMAG
# Usage: ./launch_viz.sh [type]
# Types: dashboard, map, temporal, notebook, all

set -e

echo "🚴 VéloMAG Interactive Visualizations Launcher"
echo "=============================================="

# Configuration
PYTHON_CMD="python3"
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
fi

# Fonction d'aide
show_help() {
    echo "Usage: $0 [type]"
    echo ""
    echo "Types disponibles:"
    echo "  dashboard  - Dashboard Plotly interactif"
    echo "  map        - Carte Folium interactive"
    echo "  temporal   - Analyse temporelle"
    echo "  notebook   - Jupyter Notebook complet"
    echo "  all        - Toutes les visualisations"
    echo "  help       - Affiche cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 dashboard    # Lance uniquement le dashboard"
    echo "  $0 notebook     # Ouvre le notebook Jupyter"
    echo "  $0 all          # Lance toutes les visualisations"
}

# Vérification de l'environnement
check_environment() {
    echo "🔧 Vérification de l'environnement..."
    
    if ! command -v $PYTHON_CMD &> /dev/null; then
        echo "❌ Python n'est pas installé ou accessible"
        exit 1
    fi
    
    # Vérification des dépendances principales
    $PYTHON_CMD -c "import plotly, folium, pandas" 2>/dev/null || {
        echo "❌ Dépendances manquantes. Installation..."
        $PYTHON_CMD -m pip install plotly folium pandas requests matplotlib seaborn
    }
    
    echo "✅ Environnement prêt"
}

# Lancement du dashboard
launch_dashboard() {
    echo "📊 Lancement du dashboard interactif..."
    $PYTHON_CMD interactive_viz.py
}

# Lancement du notebook
launch_notebook() {
    echo "📓 Ouverture du notebook Jupyter..."
    
    if command -v jupyter &> /dev/null; then
        jupyter notebook velomagg_analysis.ipynb
    elif command -v code &> /dev/null; then
        echo "📝 Ouverture dans VS Code..."
        code velomagg_analysis.ipynb
    else
        echo "❌ Ni Jupyter ni VS Code trouvés"
        echo "💡 Installez Jupyter: pip install jupyter"
        echo "💡 Ou utilisez VS Code avec l'extension Python"
    fi
}

# Lancement des analyses avancées
launch_advanced() {
    echo "🔬 Lancement des analyses avancées..."
    $PYTHON_CMD advanced_analytics.py
}

# Menu principal
TYPE=${1:-"all"}

case $TYPE in
    "dashboard")
        check_environment
        launch_dashboard
        ;;
    "map")
        check_environment
        echo "🗺️ Génération de la carte interactive..."
        $PYTHON_CMD -c "
from interactive_viz import InteractiveVisualizer
viz = InteractiveVisualizer()
df = viz.analyzer.analyze_current_status()
map_viz = viz.create_interactive_map(df)
map_viz.save('carte_velomagg.html')
print('✅ Carte sauvegardée: carte_velomagg.html')
import webbrowser; webbrowser.open('carte_velomagg.html')
"
        ;;
    "temporal")
        check_environment
        echo "⏰ Génération de l'analyse temporelle..."
        $PYTHON_CMD -c "
from interactive_viz import InteractiveVisualizer
viz = InteractiveVisualizer()
temporal_viz = viz.create_temporal_analysis()
temporal_viz.write_html('temporal_analysis.html')
temporal_viz.show()
print('✅ Analyse temporelle sauvegardée: temporal_analysis.html')
"
        ;;
    "notebook")
        launch_notebook
        ;;
    "advanced")
        check_environment
        launch_advanced
        ;;
    "all")
        check_environment
        echo "🎨 Lancement de toutes les visualisations..."
        launch_dashboard
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "❌ Type '$TYPE' non reconnu"
        show_help
        exit 1
        ;;
esac

echo ""
echo "🎉 Terminé! Visualisations disponibles:"
echo "  📊 dashboard_velomagg.html"
echo "  🗺️ carte_velomagg.html" 
echo "  ⏰ temporal_analysis.html"
echo "  📓 velomagg_analysis.ipynb"
