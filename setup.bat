@echo off
REM File Redaction System - Quick Deploy Script (Windows)

echo 🚀 File Redaction System Deployment Check
echo ==========================================
echo.

REM Check Python
echo ✓ Checking Python...
python --version

REM Check Node
echo ✓ Checking Node.js...
node --version

echo.
echo 📦 Installing Backend Dependencies...
cd backend
pip install -r requirements.txt

echo.
echo 📦 Installing Frontend Dependencies...
cd ..\frontend
npm install

echo.
echo ✅ Setup Complete!
echo.
echo 🎯 Next Steps:
echo 1. For LOCAL development:
echo    Backend:  cd backend ^&^& python main.py
echo    Frontend: cd frontend ^&^& npm run dev
echo.
echo 2. For DEPLOYMENT:
echo    - See DEPLOYMENT.md for detailed instructions
echo    - Backend: Deploy to Render/Railway/Heroku
echo    - Frontend: Deploy to Vercel/Netlify
echo.
echo 3. Don't forget to:
echo    - Set VITE_API_URL in frontend deployment
echo    - Check that backend is running on PORT from environment
echo.
echo 📖 For more details, read:
echo    - DEPLOYMENT.md - Deployment instructions
echo    - FIXES.md - All fixes applied
echo.

pause
