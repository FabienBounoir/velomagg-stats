#!/usr/bin/env python3
"""
Programme d'analyse des statistiques Vélomagg de Montpellier
Utilise les APIs officielles de Montpellier Métropole
"""

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import time
from typing import List, Dict, Any, Optional
import urllib.parse
import os

class VelomaggAnalyzer:
    """Classe principale pour analyser les données Vélomagg"""
    
    BASE_URL = "https://portail-api-data.montpellier3m.fr"
    STATIONS_ENDPOINT = "/bikestation"
    TIMESERIES_ENDPOINT = "/bikestation_timeseries"
    
    def __init__(self):
        self.stations_data = None
        self.timeseries_cache = {}
        
    def get_all_stations(self) -> List[Dict[str, Any]]:
        """Récupère la liste de toutes les stations"""
        try:
            response = requests.get(f"{self.BASE_URL}{self.STATIONS_ENDPOINT}")
            response.raise_for_status()
            self.stations_data = response.json()
            print(f"✅ Récupération de {len(self.stations_data)} stations")
            return self.stations_data
        except requests.RequestException as e:
            print(f"❌ Erreur lors de la récupération des stations: {e}")
            return []
    
    def get_station_timeseries(self, station_id: str, attr_name: str = "availableBikeNumber", 
                              from_date: str = "2024-01-01T00:00:00", 
                              to_date: str = "2025-01-01T00:00:00") -> Dict[str, Any]:
        """Récupère les données temporelles d'une station"""
        # URL encode the station ID
        encoded_station_id = urllib.parse.quote(station_id, safe='')
        encoded_from_date = urllib.parse.quote(from_date, safe='')
        encoded_to_date = urllib.parse.quote(to_date, safe='')
        
        url = f"{self.BASE_URL}{self.TIMESERIES_ENDPOINT}/{encoded_station_id}/attrs/{attr_name}"
        params = {
            'fromDate': from_date,
            'toDate': to_date
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Cache les données
            cache_key = f"{station_id}_{attr_name}_{from_date}_{to_date}"
            self.timeseries_cache[cache_key] = data
            
            print(f"✅ Données temporelles récupérées pour {station_id}: {len(data.get('values', []))} points")
            return data
        except requests.RequestException as e:
            print(f"❌ Erreur pour la station {station_id}: {e}")
            return {}
    
    def analyze_current_status(self) -> pd.DataFrame:
        """Analyse l'état actuel de toutes les stations"""
        if not self.stations_data:
            self.get_all_stations()
        
        stations_list = []
        for station in self.stations_data:
            station_info = {
                'id': station['id'],
                'address': station['address']['value']['streetAddress'],
                'locality': station['address']['value']['addressLocality'],
                'available_bikes': station['availableBikeNumber']['value'],
                'free_slots': station['freeSlotNumber']['value'],
                'total_slots': station['totalSlotNumber']['value'],
                'status': station['status']['value'],
                'latitude': station['location']['value']['coordinates'][1],
                'longitude': station['location']['value']['coordinates'][0],
                'last_update': station['availableBikeNumber']['metadata'].get('timestamp', {}).get('value', 'N/A')
            }
            stations_list.append(station_info)
        
        df = pd.DataFrame(stations_list)
        df['occupancy_rate'] = df['available_bikes'] / df['total_slots']
        df['utilization_rate'] = (df['total_slots'] - df['free_slots']) / df['total_slots']
        
        return df
    
    def generate_statistics_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Génère un rapport statistique complet"""
        stats = {
            'general': {
                'total_stations': len(df),
                'working_stations': len(df[df['status'] == 'working']),
                'total_bikes': df['available_bikes'].sum(),
                'total_capacity': df['total_slots'].sum(),
                'average_occupancy': df['occupancy_rate'].mean(),
                'median_occupancy': df['occupancy_rate'].median()
            },
            'distribution': {
                'bikes_per_station': {
                    'mean': df['available_bikes'].mean(),
                    'std': df['available_bikes'].std(),
                    'min': df['available_bikes'].min(),
                    'max': df['available_bikes'].max(),
                    'quartiles': df['available_bikes'].quantile([0.25, 0.5, 0.75]).to_dict()
                },
                'capacity_per_station': {
                    'mean': df['total_slots'].mean(),
                    'std': df['total_slots'].std(),
                    'min': df['total_slots'].min(),
                    'max': df['total_slots'].max()
                }
            },
            'extremes': {
                'most_occupied': df.loc[df['occupancy_rate'].idxmax()].to_dict(),
                'least_occupied': df.loc[df['occupancy_rate'].idxmin()].to_dict(),
                'largest_station': df.loc[df['total_slots'].idxmax()].to_dict(),
                'smallest_station': df.loc[df['total_slots'].idxmin()].to_dict()
            }
        }
        
        return stats
    
    def analyze_temporal_patterns(self, station_id: str, days: int = 7) -> Dict[str, Any]:
        """Analyse les patterns temporels d'une station"""
        # Calcul des dates
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days)
        
        from_date_str = from_date.strftime("%Y-%m-%dT%H:%M:%S")
        to_date_str = to_date.strftime("%Y-%m-%dT%H:%M:%S")
        
        # Récupération des données
        data = self.get_station_timeseries(station_id, "availableBikeNumber", from_date_str, to_date_str)
        
        if not data or 'values' not in data:
            return {}
        
        # Création du DataFrame
        df = pd.DataFrame({
            'timestamp': pd.to_datetime(data['index']),
            'available_bikes': data['values']
        })
        
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.day_name()
        df['date'] = df['timestamp'].dt.date
        
        analysis = {
            'hourly_patterns': df.groupby('hour')['available_bikes'].agg(['mean', 'std', 'min', 'max']).to_dict(),
            'daily_patterns': df.groupby('day_of_week')['available_bikes'].agg(['mean', 'std']).to_dict(),
            'trends': {
                'overall_trend': np.polyfit(range(len(df)), df['available_bikes'], 1)[0],
                'peak_hour': df.groupby('hour')['available_bikes'].mean().idxmin(),
                'low_hour': df.groupby('hour')['available_bikes'].mean().idxmax()
            }
        }
        
        return analysis
    
    def create_visualizations(self, df: pd.DataFrame, output_dir: str = "visualizations"):
        """Crée des visualisations des données"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Style des graphiques
        plt.style.use('seaborn-v0_8')
        
        # 1. Distribution des vélos disponibles
        plt.figure(figsize=(10, 6))
        plt.hist(df['available_bikes'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('Distribution du nombre de vélos disponibles par station')
        plt.xlabel('Nombre de vélos disponibles')
        plt.ylabel('Nombre de stations')
        plt.grid(True, alpha=0.3)
        plt.savefig(f"{output_dir}/bikes_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Taux d'occupation par station
        plt.figure(figsize=(12, 8))
        plt.scatter(df['longitude'], df['latitude'], c=df['occupancy_rate'], 
                   cmap='RdYlGn_r', s=df['total_slots']*3, alpha=0.7)
        plt.colorbar(label='Taux d\'occupation')
        plt.title('Taux d\'occupation des stations Vélomagg (taille = capacité)')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid(True, alpha=0.3)
        plt.savefig(f"{output_dir}/occupancy_map.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Top 10 des stations les plus/moins occupées
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plus occupées
        top_occupied = df.nlargest(10, 'occupancy_rate')
        ax1.barh(range(len(top_occupied)), top_occupied['occupancy_rate'])
        ax1.set_yticks(range(len(top_occupied)))
        ax1.set_yticklabels([addr[:30] + '...' if len(addr) > 30 else addr 
                            for addr in top_occupied['address']], fontsize=8)
        ax1.set_title('Top 10 stations les plus occupées')
        ax1.set_xlabel('Taux d\'occupation')
        
        # Moins occupées
        least_occupied = df.nsmallest(10, 'occupancy_rate')
        ax2.barh(range(len(least_occupied)), least_occupied['occupancy_rate'])
        ax2.set_yticks(range(len(least_occupied)))
        ax2.set_yticklabels([addr[:30] + '...' if len(addr) > 30 else addr 
                            for addr in least_occupied['address']], fontsize=8)
        ax2.set_title('Top 10 stations les moins occupées')
        ax2.set_xlabel('Taux d\'occupation')
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/top_stations.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Visualisations sauvegardées dans le dossier '{output_dir}'")
    
    def export_data(self, df: pd.DataFrame, stats: Dict[str, Any], filename: str = "velomagg_analysis"):
        """Exporte les données et statistiques"""
        # Export CSV
        df.to_csv(f"{filename}.csv", index=False, encoding='utf-8')
        
        # Export JSON des statistiques
        with open(f"{filename}_stats.json", 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Données exportées: {filename}.csv et {filename}_stats.json")

def main():
    """Fonction principale"""
    print("🚴 Démarrage de l'analyse Vélomagg Montpellier")
    
    analyzer = VelomaggAnalyzer()
    
    # 1. Récupération et analyse des données actuelles
    print("\n📊 Analyse de l'état actuel des stations...")
    current_df = analyzer.analyze_current_status()
    
    # 2. Génération des statistiques
    print("\n📈 Génération du rapport statistique...")
    stats = analyzer.generate_statistics_report(current_df)
    
    # 3. Affichage des résultats principaux
    print("\n" + "="*50)
    print("📋 RÉSUMÉ EXÉCUTIF")
    print("="*50)
    print(f"🏢 Nombre total de stations: {stats['general']['total_stations']}")
    print(f"🚴 Nombre total de vélos: {stats['general']['total_bikes']}")
    print(f"📍 Stations en fonctionnement: {stats['general']['working_stations']}")
    print(f"📊 Taux d'occupation moyen: {stats['general']['average_occupancy']:.1%}")
    print(f"🎯 Capacité totale: {stats['general']['total_capacity']} places")
    
    print(f"\n🏆 Station la plus occupée: {stats['extremes']['most_occupied']['address']}")
    print(f"   📈 Taux: {stats['extremes']['most_occupied']['occupancy_rate']:.1%}")
    
    print(f"\n🎯 Station la moins occupée: {stats['extremes']['least_occupied']['address']}")
    print(f"   📉 Taux: {stats['extremes']['least_occupied']['occupancy_rate']:.1%}")
    
    # 4. Création des visualisations
    print("\n📊 Création des visualisations...")
    analyzer.create_visualizations(current_df)
    
    # 5. Export des données
    print("\n💾 Export des données...")
    analyzer.export_data(current_df, stats)
    
    # 6. Analyse temporelle d'une station exemple
    if len(current_df) > 0:
        sample_station = current_df.iloc[0]['id']
        print(f"\n⏰ Analyse temporelle de la station exemple: {sample_station}")
        temporal_analysis = analyzer.analyze_temporal_patterns(sample_station, days=7)
        if temporal_analysis:
            print(f"🕐 Heure de pointe: {temporal_analysis['trends']['peak_hour']}h")
            print(f"🕐 Heure creuse: {temporal_analysis['trends']['low_hour']}h")
    
    print("\n✅ Analyse terminée avec succès!")
    print("📁 Fichiers générés:")
    print("   - velomagg_analysis.csv (données détaillées)")
    print("   - velomagg_analysis_stats.json (statistiques)")
    print("   - visualizations/ (graphiques)")

if __name__ == "__main__":
    main()
