#!/usr/bin/env python3
"""
Script de vérification des dépendances VéloMAG
Teste que tous les modules requis sont installés
"""

import sys
import os

# Ajouter le répertoire parent au path pour importer les modules du projet
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Teste l'importation de tous les modules requis"""
    print("🧪 Test des dépendances VéloMAG...")
    print("=" * 40)
    
    modules_to_test = [
        ("requests", "Requêtes HTTP"),
        ("pandas", "Manipulation de données"),
        ("numpy", "Calculs numériques"),
        ("matplotlib", "Graphiques statiques"),
        ("seaborn", "Visualisations statistiques"),
        ("plotly", "Graphiques interactifs"),
        ("folium", "Cartes interactives"),
        ("json", "Parsing JSON"),
        ("datetime", "Gestion des dates"),
        ("urllib.parse", "Parsing d'URLs"),
    ]
    
    failed_imports = []
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name:<15} - {description}")
        except ImportError as e:
            print(f"❌ {module_name:<15} - {description} (ERREUR: {e})")
            failed_imports.append(module_name)
    
    print("\n" + "=" * 40)
    
    if failed_imports:
        print(f"❌ {len(failed_imports)} module(s) manquant(s): {', '.join(failed_imports)}")
        print("\n🔧 Pour corriger, installez les dépendances manquantes :")
        print("pip install -r requirements.txt")
        return False
    else:
        print("✅ Tous les modules sont correctement installés!")
        
        # Test d'importation des modules spécifiques du projet
        print("\n🧪 Test des modules du projet...")
        try:
            from main import VelomaggAnalyzer
            print("✅ main.VelomaggAnalyzer")
        except ImportError as e:
            print(f"❌ main.VelomaggAnalyzer (ERREUR: {e})")
            return False
            
        try:
            from advanced_analytics import AdvancedAnalytics
            print("✅ advanced_analytics.AdvancedAnalytics")
        except ImportError as e:
            print(f"❌ advanced_analytics.AdvancedAnalytics (ERREUR: {e})")
            return False
            
        print("\n🎉 Toutes les dépendances sont OK!")
        return True

def test_api_connectivity():
    """Teste la connectivité à l'API VéloMAG"""
    print("\n🌐 Test de connectivité API...")
    try:
        import requests
        response = requests.get("https://portail-api-data.montpellier3m.fr/bikestation", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API VéloMAG accessible - {len(data)} stations disponibles")
            return True
        else:
            print(f"⚠️ API VéloMAG répond avec le code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connectivité API: {e}")
        return False

if __name__ == "__main__":
    print("🚴‍♂️ VéloMAG Stats - Vérification des dépendances")
    print("=" * 50)
    
    # Test des imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test de l'API
        api_ok = test_api_connectivity()
        
        if api_ok:
            print("\n🎯 Système prêt pour l'analyse VéloMAG!")
            sys.exit(0)
        else:
            print("\n⚠️ Problème de connectivité API mais modules OK")
            sys.exit(0)
    else:
        print("\n❌ Des dépendances sont manquantes")
        sys.exit(1)
