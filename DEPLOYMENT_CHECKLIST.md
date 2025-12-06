# 🚀 Quick Deployment Checklist

## ✅ Pre-Deployment Checklist

- [ ] Code is working locally
- [ ] Database connected to Neon
- [ ] All tests passing
- [ ] Code pushed to GitHub

---

## 📝 Render Backend Deployment

### Configuration:
```
Name: enterprise-rag-backend
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Environment Variables:
```
DATABASE_URL=postgresql://neondb_owner:npg_w7SB1leAuJMD@ep-steep-firefly-a4s5jaq7-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
GOOGLE_API_KEY=AIzaSyA5LG2SfjCFpRmOTKPLYyDlyNCResU8nRI
PINECONE_API_KEY=pcsk_6zKudz_7pyfxdHWrt3sjRQb1hD8ZmSJN7w31Cj2hEMoVTXxmc4ZwEqyZ3TCzE9Uw6WoWEd
SESSION_SECRET=super-secret-key-enterprise-rag-2024
PYTHON_VERSION=3.11.0
```

---

## 🎨 Vercel Frontend Deployment

### Configuration:
```
Framework: Vite
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
```

### Environment Variable:
```
VITE_API_URL=https://YOUR-RENDER-SERVICE.onrender.com/api/v1
```

**⚠️ Replace YOUR-RENDER-SERVICE with your actual Render service name!**

---

## 🧪 Testing URLs

After deployment, test these:

### Backend:
- Health: `https://YOUR-BACKEND.onrender.com/health`
- Docs: `https://YOUR-BACKEND.onrender.com/docs`

### Frontend:
- App: `https://YOUR-APP.vercel.app`
- Login: `admin` / `admin123`

---

## 🔄 Deployment Steps (Summary)

### 1. Render (5 minutes)
1. Go to https://dashboard.render.com
2. New Web Service → Connect GitHub repo
3. Configure settings (see above)
4. Add environment variables
5. Deploy!

### 2. Vercel (3 minutes)
1. Go to https://vercel.com
2. Import Project → Select repo
3. Set root directory to `frontend`
4. Add `VITE_API_URL` environment variable
5. Deploy!

### 3. Test (2 minutes)
1. Visit backend `/health` endpoint
2. Visit frontend URL
3. Login and test features

---

## 📞 Support Links

- Render Dashboard: https://dashboard.render.com
- Vercel Dashboard: https://vercel.com/dashboard
- Neon Dashboard: https://console.neon.tech
- Full Guide: See DEPLOYMENT_GUIDE_COMPLETE.md

---

**Total Time: ~10 minutes** ⏱️
