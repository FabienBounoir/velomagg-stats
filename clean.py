#!/usr/bin/env python3
"""
Script de nettoyage pour Vélomagg Stats
Supprime tous les fichiers générés et visualisations HTML
"""

import os
import glob
import shutil
from pathlib import Path

def clean_html_files():
    """Supprime tous les fichiers HTML générés"""
    print("🗑️  Suppression des fichiers HTML...")
    html_patterns = [
        "*.html",
        "dashboard_*.html", 
        "carte_*.html",
        "temporal_*.html",
        "visualizations/*.html"
    ]
    
    count = 0
    for pattern in html_patterns:
        for file_path in glob.glob(pattern):
            try:
                os.remove(file_path)
                print(f"   ✅ Supprimé: {file_path}")
                count += 1
            except OSError as e:
                print(f"   ⚠️  Erreur: {file_path} - {e}")
    
    return count

def clean_export_files():
    """Supprime tous les fichiers d'export"""
    print("📊 Suppression des fichiers d'export...")
    export_patterns = [
        "*.json",
        "*.csv", 
        "*.xlsx",
        "*_stats_*.json",
        "*_export_*.csv",
        "*_export_*.xlsx",
        "statistics_*.json",
        "exports/*"
    ]
    
    count = 0
    for pattern in export_patterns:
        for file_path in glob.glob(pattern):
            if not file_path.startswith(('requirements', 'package', 'setup')):
                try:
                    os.remove(file_path)
                    print(f"   ✅ Supprimé: {file_path}")
                    count += 1
                except OSError as e:
                    print(f"   ⚠️  Erreur: {file_path} - {e}")
    
    return count

def clean_directories():
    """Supprime les répertoires temporaires"""
    print("📁 Suppression des répertoires temporaires...")
    dirs_to_clean = ['exports', 'reports', 'visualizations', 'logs', '__pycache__']
    
    count = 0
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"   ✅ Supprimé: {dir_name}/")
                count += 1
            except OSError as e:
                print(f"   ⚠️  Erreur: {dir_name} - {e}")
    
    # Nettoyage des __pycache__ récursifs
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                print(f"   ✅ Supprimé: {pycache_path}")
                count += 1
            except OSError:
                pass
    
    return count

def clean_jupyter_checkpoints():
    """Supprime les checkpoints Jupyter"""
    print("📓 Suppression des checkpoints Jupyter...")
    count = 0
    
    for root, dirs, files in os.walk('.'):
        if '.ipynb_checkpoints' in dirs:
            checkpoint_path = os.path.join(root, '.ipynb_checkpoints')
            try:
                shutil.rmtree(checkpoint_path)
                print(f"   ✅ Supprimé: {checkpoint_path}")
                count += 1
            except OSError:
                pass
    
    return count

def main():
    """Fonction principale de nettoyage"""
    print("🧹 NETTOYAGE COMPLET - Vélomagg Stats")
    print("="*50)
    
    # Changement vers le répertoire du script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    total_cleaned = 0
    
    # Nettoyage par catégorie
    total_cleaned += clean_html_files()
    total_cleaned += clean_export_files()
    total_cleaned += clean_directories()
    total_cleaned += clean_jupyter_checkpoints()
    
    print("="*50)
    print(f"✅ Nettoyage terminé ! {total_cleaned} éléments supprimés")
    
    # Vérification finale
    remaining_html = glob.glob("*.html")
    if remaining_html:
        print(f"⚠️  Fichiers HTML restants: {remaining_html}")
    else:
        print("🎉 Aucun fichier HTML résiduel détecté")

if __name__ == "__main__":
    main()
