#!/usr/bin/env python3
"""Script pour mettre à jour le README avec les statistiques en temps réel"""

import json
import re
from datetime import datetime

def update_readme_stats():
    """Met à jour le README avec les statistiques actuelles"""
    
    # Lire les statistiques
    try:
        with open('docs/data/velomagg_analysis_stats.json', 'r') as f:
            stats = json.load(f)
    except FileNotFoundError:
        print("❌ Fichier de statistiques non trouvé!")
        return False
    
    # Extraire les données
    general = stats.get('general', {})
    extremes = stats.get('extremes', {})
    
    total_stations = general.get('total_stations', 0)
    total_bikes = general.get('total_bikes', 0)
    total_capacity = general.get('total_capacity', 0)
    avg_occupancy = general.get('average_occupancy', 0)
    
    most_occupied = extremes.get('most_occupied', {})
    least_occupied = extremes.get('least_occupied', {})
    
    best_station = most_occupied.get('address', 'N/A')
    best_rate = most_occupied.get('occupancy_rate', 0) * 100
    worst_station = least_occupied.get('address', 'N/A') 
    worst_rate = least_occupied.get('occupancy_rate', 0) * 100
    
    # Date actuelle
    update_date = datetime.now().strftime('%d/%m/%Y à %H:%M')
    
    print(f"📊 Mise à jour avec les statistiques :")
    print(f"   - Date: {update_date}")
    print(f"   - Stations: {total_stations}")
    print(f"   - Vélos: {total_bikes}")
    print(f"   - Occupation: {int(avg_occupancy * 100)}%")
    print(f"   - Meilleure: {best_station} ({int(best_rate)}%)")
    print(f"   - Moins occupée: {worst_station} ({int(worst_rate)}%)")
    
    # Lire le README
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ README.md non trouvé!")
        return False
    
    # Remplacements
    replacements = [
        # Date de mise à jour
        (r'\*\*Dernière mise à jour :\*\* [0-9\/]+ à [0-9:]+', 
         f'**Dernière mise à jour :** {update_date}'),
        
        # Statistiques dans le tableau
        (r'\| 🏢 \*\*Stations totales\*\* \| [0-9]+ \|',
         f'| 🏢 **Stations totales** | {total_stations} |'),
        
        (r'\| 🚴 \*\*Vélos disponibles\*\* \| [0-9]+ \|',
         f'| 🚴 **Vélos disponibles** | {total_bikes} |'),
        
        (r'\| 📍 \*\*Capacité totale\*\* \| [0-9]+ places \|',
         f'| 📍 **Capacité totale** | {total_capacity} places |'),
        
        (r'\| 📊 \*\*Taux d\'occupation\*\* \| [0-9]+% \|',
         f'| 📊 **Taux d\'occupation** | {int(avg_occupancy * 100)}% |'),
        
        # Performances des stations
        (r'\*\*Station la plus fréquentée :\*\* .+ \([0-9]+%\)',
         f'**Station la plus fréquentée :** {best_station} ({int(best_rate)}%)'),
        
        (r'\*\*Station la moins fréquentée :\*\* .+ \([0-9]+%\)',
         f'**Station la moins fréquentée :** {worst_station} ({int(worst_rate)}%)')
    ]
    
    # Appliquer les remplacements
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Sauvegarder
    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ README mis à jour avec succès!")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

if __name__ == '__main__':
    update_readme_stats()
