#!/bin/bash
# Script d'initialisation rapide pour GitHub Pages
# Usage: ./init-github-pages.sh

echo "🚀 Initialisation GitHub Pages VéloMAG"
echo "======================================"

# Vérifier si on est dans un repo git
if [ ! -d ".git" ]; then
    echo "❌ Ce dossier n'est pas un repository Git"
    echo "🔧 Initialisation du repository..."
    git init
    echo "✅ Repository Git initialisé"
fi

# Ajouter tous les fichiers
echo "📝 Ajout des fichiers au repository..."
git add .

# Commit initial si nécessaire
if [ -z "$(git log --oneline 2>/dev/null)" ]; then
    echo "📦 Commit initial..."
    git commit -m "🎉 Premier commit - Site VéloMAG Stats"
fi

# Vérifier la remote origin
if ! git remote get-url origin >/dev/null 2>&1; then
    echo ""
    echo "⚠️  Remote 'origin' non configurée"
    echo "🔧 Veuillez configurer votre repository GitHub :"
    echo ""
    echo "git remote add origin https://github.com/VOTRE-USERNAME/velomagg-stats.git"
    echo "git branch -M main"
    echo "git push -u origin main"
    echo ""
    echo "Puis activez GitHub Pages dans Settings > Pages"
    echo ""
else
    echo "📤 Push vers GitHub..."
    git push -u origin main
    
    echo ""
    echo "✅ Initialisation terminée!"
    echo ""
    echo "🌐 Prochaines étapes :"
    echo "1. Aller sur GitHub.com > Votre repository"
    echo "2. Settings > Pages"
    echo "3. Source: Deploy from a branch"
    echo "4. Branch: main, Folder: /docs"
    echo "5. Save"
    echo ""
    echo "📊 Votre site sera disponible à :"
    echo "https://$(git config user.name 2>/dev/null || echo "VOTRE-USERNAME").github.io/$(basename $(pwd))"
fi

echo ""
echo "🔄 Pour mettre à jour les données :"
echo "./update_carte.sh"
