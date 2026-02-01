# Deployment Instructions

## Backend Deployment (Render/Railway/Heroku)

### Environment Variables (Set in your deployment platform)
```
PORT=8000
DATABASE_PATH=/data/app.db
VITE_API_URL=https://your-backend-url.com
```

### Render Deployment
1. Create a new Web Service
2. Connect your GitHub repository
3. Build Command: `cd backend && pip install -r requirements.txt`
4. Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Render dashboard

### Railway Deployment
1. Create new project from GitHub
2. Settings → Root Directory: `backend`
3. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Environment variables will auto-detect or add manually

### Heroku Deployment
1. Install Heroku CLI
2. Run:
```bash
cd backend
heroku create your-app-name
git push heroku main
```

## Frontend Deployment (Vercel/Netlify)

### Vercel
1. Import project from GitHub
2. Framework Preset: Vite
3. Root Directory: `frontend`
4. Build Command: `npm run build`
5. Output Directory: `dist`
6. Environment Variables:
   - `VITE_API_URL=https://your-backend-url.com`

### Netlify
1. New site from Git
2. Base directory: `frontend`
3. Build command: `npm run build`
4. Publish directory: `frontend/dist`
5. Environment variables:
   - `VITE_API_URL=https://your-backend-url.com`

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Important Notes

1. **Update API URL**: After deploying backend, update `VITE_API_URL` in frontend environment variables
2. **CORS**: Already configured to allow all origins
3. **Database**: SQLite is used - for production, consider PostgreSQL
4. **File Storage**: Uploads stored locally - consider cloud storage (S3, Cloudinary) for production
5. **Security**: Add password hashing (bcrypt) before production use
