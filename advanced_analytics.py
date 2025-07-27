#!/usr/bin/env python3
"""
Analyses avancées pour les données Vélomagg
Module d'extensions pour des analyses spécialisées
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

class AdvancedAnalytics:
    """Analyses avancées des données Vélomagg"""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
    
    def predict_peak_hours(self, station_id: str, days: int = 30) -> Dict[str, Any]:
        """Prédit les heures de pointe basées sur l'historique"""
        data = self.analyzer.get_station_timeseries(
            station_id, "availableBikeNumber", 
            (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S"),
            datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        )
        
        if not data or 'values' not in data:
            return {}
        
        df = pd.DataFrame({
            'timestamp': pd.to_datetime(data['index']),
            'available_bikes': data['values']
        })
        
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6])
        
        # Calcul de l'occupation inverse (plus de vélos pris = heure de pointe)
        max_bikes = df['available_bikes'].max()
        df['usage_intensity'] = max_bikes - df['available_bikes']
        
        # Patterns par type de jour
        weekday_pattern = df[~df['is_weekend']].groupby('hour')['usage_intensity'].mean()
        weekend_pattern = df[df['is_weekend']].groupby('hour')['usage_intensity'].mean()
        
        return {
            'weekday_peaks': {
                'morning_peak': weekday_pattern.idxmax(),
                'evening_peak': weekday_pattern[weekday_pattern.index > 12].idxmax(),
                'pattern': weekday_pattern.to_dict()
            },
            'weekend_peaks': {
                'main_peak': weekend_pattern.idxmax(),
                'pattern': weekend_pattern.to_dict()
            },
            'predictions': {
                'next_weekday_peak': weekday_pattern.idxmax(),
                'next_weekend_peak': weekend_pattern.idxmax()
            }
        }
    
    def calculate_station_efficiency(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcule l'efficacité des stations"""
        df_copy = df.copy()
        
        # Taux d'utilisation (vélos + places occupées / capacité totale)
        df_copy['utilization_rate'] = (df_copy['total_slots'] - df_copy['free_slots']) / df_copy['total_slots']
        
        # Score d'équilibre (proche de 50% = optimal)
        df_copy['balance_score'] = 1 - abs(df_copy['occupancy_rate'] - 0.5) * 2
        
        # Score de disponibilité (évite les stations vides/pleines)
        df_copy['availability_score'] = np.where(
            (df_copy['available_bikes'] == 0) | (df_copy['free_slots'] == 0), 0, 1
        )
        
        # Score d'efficacité global
        df_copy['efficiency_score'] = (
            df_copy['balance_score'] * 0.4 + 
            df_copy['availability_score'] * 0.3 +
            df_copy['utilization_rate'] * 0.3
        )
        
        return df_copy
    
    def identify_problem_stations(self, df: pd.DataFrame) -> Dict[str, List[Dict]]:
        """Identifie les stations problématiques"""
        df_eff = self.calculate_station_efficiency(df)
        
        problems = {
            'always_empty': df_eff[df_eff['available_bikes'] == 0].to_dict('records'),
            'always_full': df_eff[df_eff['free_slots'] == 0].to_dict('records'),
            'low_efficiency': df_eff[df_eff['efficiency_score'] < 0.3].to_dict('records'),
            'inactive': df_eff[df_eff['status'] != 'working'].to_dict('records'),
            'oversized': df_eff[df_eff['utilization_rate'] < 0.1].to_dict('records'),
            'undersized': df_eff[df_eff['utilization_rate'] > 0.9].to_dict('records')
        }
        
        return problems
    
    def calculate_coverage_analysis(self, df: pd.DataFrame, radius_km: float = 0.5) -> Dict[str, Any]:
        """Analyse de couverture géographique"""
        from math import radians, cos, sin, asin, sqrt
        
        def haversine(lon1, lat1, lon2, lat2):
            """Calcule la distance entre deux points GPS"""
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            r = 6371  # Rayon terrestre en km
            return c * r
        
        # Calcul des distances entre stations
        distances = []
        coverage_zones = []
        
        for i, station1 in df.iterrows():
            nearby_stations = 0
            for j, station2 in df.iterrows():
                if i != j:
                    dist = haversine(
                        station1['longitude'], station1['latitude'],
                        station2['longitude'], station2['latitude']
                    )
                    if dist <= radius_km:
                        nearby_stations += 1
                    distances.append(dist)
            
            coverage_zones.append({
                'station_id': station1['id'],
                'address': station1['address'],
                'nearby_stations': nearby_stations,
                'coverage_density': nearby_stations / (np.pi * radius_km**2)
            })
        
        coverage_df = pd.DataFrame(coverage_zones)
        
        return {
            'average_distance': np.mean(distances),
            'min_distance': np.min(distances),
            'isolated_stations': coverage_df[coverage_df['nearby_stations'] == 0].to_dict('records'),
            'dense_areas': coverage_df[coverage_df['nearby_stations'] > 5].to_dict('records'),
            'coverage_stats': {
                'mean_density': coverage_df['coverage_density'].mean(),
                'std_density': coverage_df['coverage_density'].std()
            }
        }
    
    def generate_optimization_recommendations(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Génère des recommandations d'optimisation"""
        problems = self.identify_problem_stations(df)
        df_eff = self.calculate_station_efficiency(df)
        
        recommendations = {
            'urgent': [],
            'maintenance': [],
            'capacity': [],
            'deployment': []
        }
        
        # Recommandations urgentes
        if len(problems['inactive']) > 0:
            recommendations['urgent'].append(
                f"🚨 {len(problems['inactive'])} stations hors service nécessitent une intervention immédiate"
            )
        
        if len(problems['always_empty']) > 0:
            recommendations['urgent'].append(
                f"⚠️ {len(problems['always_empty'])} stations complètement vides (redistribution urgente)"
            )
        
        if len(problems['always_full']) > 0:
            recommendations['urgent'].append(
                f"⚠️ {len(problems['always_full'])} stations complètement pleines (retrait urgent)"
            )
        
        # Recommandations de maintenance
        low_eff_count = len(problems['low_efficiency'])
        if low_eff_count > len(df) * 0.1:
            recommendations['maintenance'].append(
                f"🔧 {low_eff_count} stations ont une faible efficacité (>10% du réseau)"
            )
        
        # Recommandations de capacité
        if len(problems['oversized']) > 0:
            recommendations['capacity'].append(
                f"📉 {len(problems['oversized'])} stations sous-utilisées (réduction possible)"
            )
        
        if len(problems['undersized']) > 0:
            recommendations['capacity'].append(
                f"📈 {len(problems['undersized'])} stations sur-utilisées (extension recommandée)"
            )
        
        # Recommandations de déploiement
        avg_efficiency = df_eff['efficiency_score'].mean()
        if avg_efficiency < 0.6:
            recommendations['deployment'].append(
                f"🎯 Efficacité réseau globale faible ({avg_efficiency:.1%}) - rééquilibrage nécessaire"
            )
        
        return recommendations

class ReportGenerator:
    """Générateur de rapports avancés"""
    
    def __init__(self, analyzer, advanced_analytics):
        self.analyzer = analyzer
        self.advanced = advanced_analytics
    
    def generate_executive_summary(self, df: pd.DataFrame) -> str:
        """Génère un résumé exécutif"""
        stats = self.analyzer.generate_statistics_report(df)
        problems = self.advanced.identify_problem_stations(df)
        recommendations = self.advanced.generate_optimization_recommendations(df)
        
        summary = f"""
📊 RAPPORT EXÉCUTIF VÉLOMAGG MONTPELLIER
{'='*50}

🎯 INDICATEURS CLÉS
• Réseau: {stats['general']['total_stations']} stations ({stats['general']['working_stations']} actives)
• Flotte: {stats['general']['total_bikes']} vélos sur {stats['general']['total_capacity']} places
• Taux d'occupation: {stats['general']['average_occupancy']:.1%} (cible: 40-60%)
• Performance réseau: {'🟢 BONNE' if stats['general']['average_occupancy'] > 0.4 and stats['general']['average_occupancy'] < 0.6 else '🟡 À SURVEILLER' if stats['general']['average_occupancy'] > 0.2 else '🔴 CRITIQUE'}

⚠️ ALERTES ({len(problems['inactive']) + len(problems['always_empty']) + len(problems['always_full'])} urgentes)
• Stations hors service: {len(problems['inactive'])}
• Stations vides: {len(problems['always_empty'])}
• Stations pleines: {len(problems['always_full'])}
• Efficacité faible: {len(problems['low_efficiency'])}

🏆 PERFORMANCES
• Meilleure station: {stats['extremes']['most_occupied']['address'][:40]}... ({stats['extremes']['most_occupied']['occupancy_rate']:.1%})
• Station critique: {stats['extremes']['least_occupied']['address'][:40]}... ({stats['extremes']['least_occupied']['occupancy_rate']:.1%})

💡 ACTIONS PRIORITAIRES
"""
        
        for category, items in recommendations.items():
            if items:
                summary += f"\n{category.upper()}:\n"
                for item in items[:3]:  # Top 3 par catégorie
                    summary += f"  • {item}\n"
        
        return summary
    
    def generate_detailed_report(self, df: pd.DataFrame, output_file: str = "rapport_detaille.txt"):
        """Génère un rapport détaillé complet"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_executive_summary(df))
            f.write("\n\n" + "="*50)
            f.write("\nRAPPORT DÉTAILLÉ\n")
            f.write("="*50)
            
            # Analyse par quartiles
            f.write(f"\n\n📈 ANALYSE PAR QUARTILES\n")
            f.write(f"Q1 (25%): {df['occupancy_rate'].quantile(0.25):.1%}\n")
            f.write(f"Q2 (50%): {df['occupancy_rate'].quantile(0.5):.1%}\n")
            f.write(f"Q3 (75%): {df['occupancy_rate'].quantile(0.75):.1%}\n")
            
            # Top/Bottom stations
            f.write(f"\n\n🏆 TOP 10 STATIONS LES PLUS EFFICACES\n")
            df_eff = self.advanced.calculate_station_efficiency(df)
            top_stations = df_eff.nlargest(10, 'efficiency_score')
            for i, station in top_stations.iterrows():
                f.write(f"{station['address'][:50]:<50} {station['efficiency_score']:.1%}\n")
            
            f.write(f"\n\n⚠️ TOP 10 STATIONS À AMÉLIORER\n")
            bottom_stations = df_eff.nsmallest(10, 'efficiency_score')
            for i, station in bottom_stations.iterrows():
                f.write(f"{station['address'][:50]:<50} {station['efficiency_score']:.1%}\n")
        
        print(f"✅ Rapport détaillé sauvegardé: {output_file}")

def main_advanced():
    """Fonction principale pour les analyses avancées"""
    from main import VelomaggAnalyzer
    
    print("🔬 Démarrage des analyses avancées Vélomagg")
    
    # Initialisation
    analyzer = VelomaggAnalyzer()
    advanced = AdvancedAnalytics(analyzer)
    reporter = ReportGenerator(analyzer, advanced)
    
    # Récupération des données
    df = analyzer.analyze_current_status()
    
    # Analyses avancées
    print("\n🧠 Calcul de l'efficacité des stations...")
    df_efficiency = advanced.calculate_station_efficiency(df)
    
    print("🔍 Identification des problèmes...")
    problems = advanced.identify_problem_stations(df)
    
    print("📍 Analyse de couverture géographique...")
    coverage = advanced.calculate_coverage_analysis(df)
    
    print("💡 Génération des recommandations...")
    recommendations = advanced.generate_optimization_recommendations(df)
    
    # Rapport exécutif
    print("\n📊 Génération du rapport exécutif...")
    exec_summary = reporter.generate_executive_summary(df)
    print(exec_summary)
    
    # Rapport détaillé
    print("\n📄 Génération du rapport détaillé...")
    reporter.generate_detailed_report(df)
    
    # Analyse temporelle sur quelques stations
    print("\n⏰ Analyse des patterns temporels...")
    sample_stations = df.head(3)['id'].tolist()
    for station_id in sample_stations:
        peaks = advanced.predict_peak_hours(station_id, days=7)
        if peaks:
            print(f"Station {station_id}: Pic semaine {peaks['weekday_peaks']['morning_peak']}h-{peaks['weekday_peaks']['evening_peak']}h")
    
    print("\n✅ Analyses avancées terminées!")

if __name__ == "__main__":
    main_advanced()
