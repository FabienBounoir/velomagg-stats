#!/usr/bin/env python3
"""
Script de nettoyage rapide pour les notebooks Jupyter
Supprime uniquement les fichiers HTML sans toucher aux caches Python
"""

import os
import glob
from pathlib import Path

def clean_html_only():
    """Supprime uniquement les fichiers HTML générés"""
    print("🗑️  Nettoyage rapide - Suppression des fichiers HTML...")
    
    # Patterns spécifiques aux visualisations HTML
    html_patterns = [
        "dashboard_*.html",
        "carte_*.html", 
        "temporal_*.html",
        "*.html"
    ]
    
    count = 0
    for pattern in html_patterns:
        for file_path in glob.glob(pattern):
            # Éviter de supprimer les fichiers HTML importants comme index.html
            if not file_path.startswith(('index', 'README', 'doc')):
                try:
                    os.remove(file_path)
                    print(f"   ✅ Supprimé: {file_path}")
                    count += 1
                except OSError as e:
                    print(f"   ⚠️  Erreur: {file_path} - {e}")
    
    return count

def main():
    """Fonction principale de nettoyage rapide"""
    print("🧹 NETTOYAGE RAPIDE - Fichiers HTML seulement")
    print("="*45)
    
    # Changement vers le répertoire du script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Nettoyage HTML uniquement
    total_cleaned = clean_html_only()
    
    print("="*45)
    if total_cleaned > 0:
        print(f"✅ Nettoyage rapide terminé ! {total_cleaned} fichiers HTML supprimés")
    else:
        print("🎉 Aucun fichier HTML à supprimer")
    
    # Vérification finale
    remaining_html = [f for f in glob.glob("*.html") if not f.startswith(('index', 'README', 'doc'))]
    if remaining_html:
        print(f"ℹ️  Fichiers HTML restants (non supprimés): {remaining_html}")

if __name__ == "__main__":
    main()
