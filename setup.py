#!/usr/bin/env python3
"""
Script de configuration et de test pour Vélomagg Stats
"""

import subprocess
import sys
import os

def install_requirements():
    """Installe les dépendances Python"""
    print("📦 Installation des dépendances...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False

def test_apis():
    """Teste la connectivité aux APIs"""
    print("\n🌐 Test de connectivité aux APIs...")
    try:
        import requests
        
        # Test API stations
        response = requests.get("https://portail-api-data.montpellier3m.fr/bikestation", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Stations OK - {len(data)} stations détectées")
        else:
            print(f"❌ API Stations échec - Code: {response.status_code}")
            return False
        
        # Test API timeseries avec une station
        if data:
            station_id = data[0]['id']
            encoded_id = requests.utils.quote(station_id, safe='')
            url = f"https://portail-api-data.montpellier3m.fr/bikestation_timeseries/{encoded_id}/attrs/availableBikeNumber"
            params = {
                'fromDate': '2024-07-20T00:00:00',
                'toDate': '2024-07-27T00:00:00'
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                timeseries_data = response.json()
                print(f"✅ API Timeseries OK - {len(timeseries_data.get('values', []))} points de données")
            else:
                print(f"⚠️ API Timeseries partiellement disponible - Code: {response.status_code}")
        
        return True
        
    except ImportError:
        print("❌ Module requests non installé")
        return False
    except Exception as e:
        print(f"❌ Erreur de connectivité: {e}")
        return False

def create_directories():
    """Crée les répertoires nécessaires"""
    print("\n📁 Création des répertoires...")
    directories = ['visualizations', 'exports', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Répertoire '{directory}' créé")

def run_basic_test():
    """Lance un test basique du programme"""
    print("\n🧪 Test basique du programme...")
    try:
        from main import VelomaggAnalyzer
        
        analyzer = VelomaggAnalyzer()
        stations = analyzer.get_all_stations()
        
        if stations:
            print(f"✅ Test réussi - {len(stations)} stations récupérées")
            
            # Test d'une analyse basique
            df = analyzer.analyze_current_status()
            stats = analyzer.generate_statistics_report(df)
            
            print(f"📊 Statistiques générées:")
            print(f"   - {stats['general']['total_stations']} stations totales")
            print(f"   - {stats['general']['total_bikes']} vélos disponibles")
            print(f"   - {stats['general']['average_occupancy']:.1%} taux d'occupation moyen")
            
            return True
        else:
            print("❌ Aucune station récupérée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def main():
    """Fonction principale de configuration"""
    print("🚴 Configuration Vélomagg Stats")
    print("="*40)
    
    # Étape 1: Installation
    if not install_requirements():
        print("\n❌ Configuration échouée lors de l'installation")
        return False
    
    # Étape 2: Test APIs
    if not test_apis():
        print("\n⚠️ APIs partiellement disponibles - le programme peut fonctionner en mode dégradé")
    
    # Étape 3: Création répertoires
    create_directories()
    
    # Étape 4: Test basique
    if not run_basic_test():
        print("\n❌ Configuration échouée lors du test")
        return False
    
    print("\n✅ Configuration terminée avec succès!")
    print("\n📋 Commandes disponibles:")
    print("   python main.py                 # Analyse standard")
    print("   python advanced_analytics.py   # Analyses avancées")
    print("   python setup.py               # Re-configuration")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
