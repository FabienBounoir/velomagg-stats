#!/bin/bash
# Test du workflow de mise à jour automatique

echo "🧪 Test de mise à jour automatique du README et docs"
echo "=================================================="

# Vérifier que les fichiers de données existent
if [ ! -f "velomagg_analysis_stats.json" ]; then
    echo "❌ Fichier velomagg_analysis_stats.json manquant"
    echo "🔧 Génération des données..."
    .venv/bin/python main.py
fi

# Extraire les statistiques avec jq (plus fiable)
if command -v jq >/dev/null 2>&1; then
    TOTAL_STATIONS=$(cat velomagg_analysis_stats.json | jq -r '.general.total_stations')
    TOTAL_BIKES=$(cat velomagg_analysis_stats.json | jq -r '.general.total_bikes')
    OCCUPATION=$(cat velomagg_analysis_stats.json | jq -r '.general.average_occupancy')
    WORKING_STATIONS=$(cat velomagg_analysis_stats.json | jq -r '.general.working_stations')
else
    echo "⚠️ jq non installé, utilisation de grep (moins fiable)"
    TOTAL_STATIONS=$(cat velomagg_analysis_stats.json | grep -A1 '"total_stations"' | grep -o '[0-9]*' | head -1)
    TOTAL_BIKES=$(cat velomagg_analysis_stats.json | grep -A1 '"total_bikes"' | grep -o '[0-9]*' | head -1)
    OCCUPATION=$(cat velomagg_analysis_stats.json | grep -A1 '"average_occupancy"' | grep -o '[0-9.]*' | head -1)
    WORKING_STATIONS=$(cat velomagg_analysis_stats.json | grep -A1 '"working_stations"' | grep -o '[0-9]*' | head -1)
fi

echo "📊 Statistiques extraites:"
echo "  🚲 Stations: $TOTAL_STATIONS"
echo "  🚴‍♂️ Vélos: $TOTAL_BIKES"
echo "  🔧 Actives: $WORKING_STATIONS"
echo "  📍 Occupation: $OCCUPATION"

# Calculer le pourcentage
OCCUPATION_PERCENT=$(echo "$OCCUPATION * 100" | bc -l | cut -d'.' -f1)
echo "  📊 Occupation %: $OCCUPATION_PERCENT%"

# Test de mise à jour du README
echo ""
echo "📝 Test mise à jour README..."

# Créer une sauvegarde
cp README.md README.md.backup

# Mettre à jour les chiffres dans le README
sed -i.bak "s/les \*\*[0-9]* stations VéloMAG\*\*/les **$TOTAL_STATIONS stations VéloMAG**/" README.md

echo "✅ README mis à jour avec les vraies données"

# Test de mise à jour du site
echo ""
echo "🌐 Test mise à jour site web..."

if [ -f "docs/index.html" ]; then
    # Formater l'occupation avec 1 décimale
    OCCUPATION_FORMATTED=$(echo "$OCCUPATION * 100" | bc -l | cut -d'.' -f1).$(echo "$OCCUPATION * 100" | bc -l | cut -d'.' -f2 | cut -c1)
    
    # Mise à jour du HTML
    sed -i.bak "s/<h3 class=\"text-primary mb-1\" id=\"total-stations\">[0-9]*<\/h3>/<h3 class=\"text-primary mb-1\" id=\"total-stations\">$TOTAL_STATIONS<\/h3>/" docs/index.html
    sed -i.bak "s/<h3 class=\"text-success mb-1\" id=\"total-bikes\">[0-9]*<\/h3>/<h3 class=\"text-success mb-1\" id=\"total-bikes\">$TOTAL_BIKES<\/h3>/" docs/index.html
    sed -i.bak "s/<h3 class=\"text-info mb-1\" id=\"occupation-rate\">[0-9.]*%<\/h3>/<h3 class=\"text-info mb-1\" id=\"occupation-rate\">$OCCUPATION_FORMATTED%<\/h3>/" docs/index.html
    
    echo "✅ Site web mis à jour avec les vraies données"
else
    echo "⚠️ docs/index.html non trouvé - exécuter ./organize_files.sh d'abord"
fi

echo ""
echo "📈 Créer section statistiques temps réel..."

# Créer la section de stats
cat > /tmp/stats_section.md << EOF

## 📈 Statistiques en temps réel

> **Dernière mise à jour :** $(date '+%d/%m/%Y à %H:%M UTC')

| 📊 Métrique | 🔢 Valeur | 📝 Description |
|-------------|-----------|----------------|
| 🚲 **Stations actives** | **$WORKING_STATIONS/$TOTAL_STATIONS** | Stations en fonctionnement |
| 🚴‍♂️ **Vélos disponibles** | **$TOTAL_BIKES** | Total des vélos en circulation |
| 📍 **Taux d'occupation** | **$OCCUPATION_PERCENT%** | Moyenne de toutes les stations |
| 🔄 **Mise à jour** | **2x/jour** | 8h et 20h UTC automatique |

EOF

echo "✅ Section de statistiques créée"
cat /tmp/stats_section.md

echo ""
echo "🔄 Pour restaurer le README original:"
echo "mv README.md.backup README.md"

echo ""
echo "✅ Test terminé!"
