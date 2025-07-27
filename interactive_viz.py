#!/usr/bin/env python3
"""
Script pour lancer uniquement les visualisations interactives
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import VelomaggAnalyzer
from advanced_analytics import AdvancedAnalytics
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium import plugins
import webbrowser

class InteractiveVisualizer:
    """Générateur de visualisations interactives"""
    
    def __init__(self):
        self.analyzer = VelomaggAnalyzer()
        self.advanced = AdvancedAnalytics(self.analyzer)
        
    def create_plotly_dashboard(self, df):
        """Crée un dashboard Plotly interactif"""
        print("📊 Création du dashboard Plotly...")
        
        # Création des sous-graphiques
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Distribution des vélos disponibles',
                'Taux d\'occupation vs Capacité',
                'Scores d\'efficacité par station',
                'Répartition des statuts'
            ),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "box"}, {"type": "pie"}]]
        )
        
        # 1. Histogramme des vélos disponibles
        fig.add_trace(
            go.Histogram(
                x=df['available_bikes'],
                nbinsx=20,
                name='Vélos disponibles',
                marker_color='lightblue',
                opacity=0.7
            ),
            row=1, col=1
        )
        
        # 2. Scatter plot occupation vs capacité
        fig.add_trace(
            go.Scatter(
                x=df['total_slots'],
                y=df['occupancy_rate'],
                mode='markers',
                marker=dict(
                    size=df['available_bikes'],
                    color=df['occupancy_rate'],
                    colorscale='RdYlGn_r',
                    showscale=True,
                    colorbar=dict(title="Taux d'occupation")
                ),
                text=df['address'],
                hovertemplate='<b>%{text}</b><br>Capacité: %{x}<br>Occupation: %{y:.1%}<br>Vélos: %{marker.size}<extra></extra>',
                name='Stations'
            ),
            row=1, col=2
        )
        
        # 3. Box plot des scores d'efficacité
        df_eff = self.advanced.calculate_station_efficiency(df)
        fig.add_trace(
            go.Box(
                y=df_eff['efficiency_score'],
                name='Efficacité',
                marker_color='lightgreen'
            ),
            row=2, col=1
        )
        
        # 4. Pie chart des statuts
        status_counts = df['status'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                name='Statuts'
            ),
            row=2, col=2
        )
        
        # Mise en page
        fig.update_layout(
            title_text="🚴 Dashboard VéloMAG Montpellier - Analyses Interactives",
            title_x=0.5,
            height=800,
            showlegend=False
        )
        
        # Labels des axes
        fig.update_xaxes(title_text="Nombre de vélos", row=1, col=1)
        fig.update_yaxes(title_text="Fréquence", row=1, col=1)
        
        fig.update_xaxes(title_text="Capacité totale", row=1, col=2)
        fig.update_yaxes(title_text="Taux d'occupation", row=1, col=2)
        
        fig.update_yaxes(title_text="Score d'efficacité", row=2, col=1)
        
        return fig
    
    def create_interactive_map(self, df):
        """Crée une carte Folium interactive"""
        print("🗺️ Création de la carte interactive...")
        
        # Centre sur Montpellier
        center_lat = df['latitude'].mean()
        center_lon = df['longitude'].mean()
        
        # Création de la carte
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=13,
            tiles='OpenStreetMap'
        )
        
        # Ajout des stations
        for idx, station in df.iterrows():
            # Couleur selon l'occupation
            if station['occupancy_rate'] > 0.8:
                color = 'red'
                icon = 'exclamation-sign'
            elif station['occupancy_rate'] > 0.6:
                color = 'orange'
                icon = 'warning-sign'
            elif station['occupancy_rate'] > 0.3:
                color = 'green'
                icon = 'ok-sign'
            else:
                color = 'blue'
                icon = 'info-sign'
            
            # Pop-up avec informations
            popup_html = f"""
            <div style="width: 250px;">
                <h4>🚴 {station['address'][:50]}...</h4>
                <hr>
                <b>📊 État actuel:</b><br>
                • Vélos disponibles: <span style="color: green;">{station['available_bikes']}</span><br>
                • Places libres: <span style="color: blue;">{station['free_slots']}</span><br>
                • Capacité totale: {station['total_slots']}<br>
                • Taux d'occupation: <span style="color: {'red' if station['occupancy_rate'] > 0.8 else 'orange' if station['occupancy_rate'] > 0.5 else 'green'};">{station['occupancy_rate']:.1%}</span><br>
                <hr>
                <b>🔧 Statut:</b> {station['status']}<br>
                <b>📍 Coordonnées:</b> {station['latitude']:.4f}, {station['longitude']:.4f}
            </div>
            """
            
            folium.Marker(
                [station['latitude'], station['longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=color, icon=icon, prefix='glyphicon'),
                tooltip=f"{station['address'][:30]}... - {station['available_bikes']} vélos"
            ).add_to(m)
        
        # Ajout d'une heatmap de densité
        heat_data = [[row['latitude'], row['longitude'], row['available_bikes']] 
                     for idx, row in df.iterrows()]
        
        plugins.HeatMap(heat_data, radius=15, blur=10, gradient={
            0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'
        }).add_to(m)
        
        # Contrôles de couches
        folium.LayerControl().add_to(m)
        
        return m
    
    def create_temporal_analysis(self, station_ids=None, days=7):
        """Crée une analyse temporelle interactive"""
        print("⏰ Analyse temporelle interactive...")
        
        if not station_ids:
            # Prendre un échantillon de stations
            df = self.analyzer.analyze_current_status()
            station_ids = df.head(3)['id'].tolist()
        
        fig = go.Figure()
        colors = px.colors.qualitative.Set1
        
        for i, station_id in enumerate(station_ids):
            peaks = self.advanced.predict_peak_hours(station_id, days=days)
            
            if peaks and 'weekday_peaks' in peaks:
                pattern = peaks['weekday_peaks']['pattern']
                hours = list(pattern.keys())
                usage = list(pattern.values())
                
                # Obtenir l'adresse de la station
                df = self.analyzer.analyze_current_status()
                station_info = df[df['id'] == station_id]
                station_name = station_info['address'].iloc[0][:30] + "..." if not station_info.empty else f"Station {station_id}"
                
                fig.add_trace(
                    go.Scatter(
                        x=hours,
                        y=usage,
                        mode='lines+markers',
                        name=station_name,
                        line=dict(color=colors[i % len(colors)], width=3),
                        hovertemplate=f'<b>{station_name}</b><br>Heure: %{{x}}h<br>Intensité d\'usage: %{{y:.1f}}<extra></extra>'
                    )
                )
        
        fig.update_layout(
            title="⏰ Patterns d'usage horaire - Stations VéloMAG",
            xaxis_title="Heure de la journée",
            yaxis_title="Intensité d'usage (vélos pris)",
            template="plotly_white",
            height=500,
            hovermode='x unified'
        )
        
        return fig

def main_interactive():
    """Fonction principale pour les visualisations interactives"""
    print("🎨 Lancement des visualisations interactives VéloMAG")
    
    viz = InteractiveVisualizer()
    
    # Récupération des données
    print("\n📡 Récupération des données...")
    df = viz.analyzer.analyze_current_status()
    
    # 1. Dashboard Plotly
    print("\n📊 Génération du dashboard interactif...")
    dashboard = viz.create_plotly_dashboard(df)
    dashboard.write_html("dashboard_velomagg.html")
    print("✅ Dashboard sauvegardé: dashboard_velomagg.html")
    
    # 2. Carte interactive
    print("\n🗺️ Génération de la carte interactive...")
    map_viz = viz.create_interactive_map(df)
    map_viz.save("carte_velomagg.html")
    print("✅ Carte sauvegardée: carte_velomagg.html")
    
    # 3. Analyse temporelle
    print("\n⏰ Génération de l'analyse temporelle...")
    temporal_viz = viz.create_temporal_analysis()
    temporal_viz.write_html("temporal_analysis.html")
    print("✅ Analyse temporelle sauvegardée: temporal_analysis.html")
    
    print("\n✅ Visualisations générées:")
    print("  📊 dashboard_velomagg.html - Dashboard principal")
    print("  🗺️ carte_velomagg.html - Carte interactive")  
    print("  ⏰ temporal_analysis.html - Analyse temporelle")
    
    # Ouverture automatique dans le navigateur
    print("\n🌐 Ouverture automatique dans le navigateur...")
    webbrowser.open("dashboard_velomagg.html")
    
    return dashboard, map_viz, temporal_viz

if __name__ == "__main__":
    main_interactive()
