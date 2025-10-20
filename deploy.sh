#!/bin/bash

# AgriPool Deployment Script

echo "🚀 AgriPool Deployment Script"
echo "=============================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: AgriPool platform"
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

echo ""
echo "📋 Next Steps:"
echo ""
echo "1️⃣  Push to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/agripool.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "2️⃣  Deploy to Railway (Recommended):"
echo "   - Go to https://railway.app"
echo "   - Sign up with GitHub"
echo "   - Click 'New Project' → 'Deploy from GitHub repo'"
echo "   - Select your repository"
echo "   - Done! 🎉"
echo ""
echo "3️⃣  Or deploy to Render:"
echo "   - Go to https://render.com"
echo "   - New → Web Service"
echo "   - Connect GitHub repo"
echo "   - Deploy!"
echo ""
echo "📖 Full deployment guide: See DEPLOYMENT.md"
echo ""
