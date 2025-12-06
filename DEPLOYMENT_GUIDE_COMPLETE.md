# 🚀 Complete Deployment Guide: Render + Vercel

## Prerequisites

✅ GitHub account  
✅ Render account (free): https://dashboard.render.com  
✅ Vercel account (free): https://vercel.com  
✅ Your code pushed to GitHub  

---

## Part 1: Push Code to GitHub

### Step 1: Initialize Git (if not already done)

```bash
cd d:\enterprise-rag
git add .
git commit -m "Ready for deployment with Neon database"
git push origin main
```

If you haven't created a GitHub repository yet:

1. Go to https://github.com/new
2. Create a new repository (e.g., "enterprise-rag")
3. Copy the repository URL
4. Run:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/enterprise-rag.git
   git branch -M main
   git push -u origin main
   ```

---

## Part 2: Deploy Backend to Render

### Step 1: Sign Up / Log In to Render

1. Go to **https://dashboard.render.com**
2. Sign up with GitHub (recommended) or email
3. Authorize Render to access your GitHub repositories

### Step 2: Create New Web Service

1. Click **"New +"** button → **"Web Service"**
2. Connect your GitHub repository:
   - Click **"Connect account"** if needed
   - Select your **enterprise-rag** repository
   - Click **"Connect"**

### Step 3: Configure Backend Service

Fill in the following settings:

**Basic Settings:**
- **Name**: `enterprise-rag-backend` (or any name you like)
- **Region**: Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```

- **Start Command**:
  ```
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- Select **"Free"** (0.1 CPU, 512 MB RAM)

### Step 4: Add Environment Variables

Scroll down to **"Environment Variables"** section and add these:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://neondb_owner:npg_w7SB1leAuJMD@ep-steep-firefly-a4s5jaq7-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require` |
| `GOOGLE_API_KEY` | `AIzaSyA5LG2SfjCFpRmOTKPLYyDlyNCResU8nRI` |
| `PINECONE_API_KEY` | `pcsk_6zKudz_7pyfxdHWrt3sjRQb1hD8ZmSJN7w31Cj2hEMoVTXxmc4ZwEqyZ3TCzE9Uw6WoWEd` |
| `SESSION_SECRET` | `super-secret-key-enterprise-rag-2024` |
| `PYTHON_VERSION` | `3.11.0` |

**How to add:**
1. Click **"Add Environment Variable"**
2. Enter Key and Value
3. Repeat for all variables

### Step 5: Deploy!

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Watch the logs - you should see:
   ```
   ✓ Using PostgreSQL database
   Default admin user created: admin / admin123
   ```

### Step 6: Get Your Backend URL

After deployment completes:
- Your backend URL will be: `https://enterprise-rag-backend.onrender.com`
- Test it: `https://enterprise-rag-backend.onrender.com/health`
- Should return: `{"status": "healthy"}`

**⚠️ IMPORTANT**: Copy this URL! You'll need it for Vercel.

---

## Part 3: Deploy Frontend to Vercel

### Step 1: Sign Up / Log In to Vercel

1. Go to **https://vercel.com**
2. Click **"Sign Up"** or **"Log In"**
3. Sign up with GitHub (recommended)
4. Authorize Vercel to access your repositories

### Step 2: Import Project

1. Click **"Add New..."** → **"Project"**
2. Find your **enterprise-rag** repository
3. Click **"Import"**

### Step 3: Configure Project

**Project Settings:**
- **Framework Preset**: Vite (should auto-detect)
- **Root Directory**: `frontend`
- **Build Command**: `npm run build` (auto-filled)
- **Output Directory**: `dist` (auto-filled)

### Step 4: Add Environment Variable

Click **"Environment Variables"** and add:

| Name | Value |
|------|-------|
| `VITE_API_URL` | `https://enterprise-rag-backend.onrender.com/api/v1` |

**⚠️ Replace** `enterprise-rag-backend` with YOUR actual Render service name!

**Format must be**: `https://YOUR-RENDER-SERVICE.onrender.com/api/v1`

### Step 5: Deploy!

1. Click **"Deploy"**
2. Wait for deployment (2-3 minutes)
3. Vercel will build and deploy your frontend

### Step 6: Get Your Frontend URL

After deployment:
- Your app URL will be: `https://enterprise-rag-xxx.vercel.app`
- Click **"Visit"** to open your deployed app!

---

## Part 4: Test Your Deployed Application

### Test Backend

1. Visit: `https://YOUR-BACKEND.onrender.com/health`
2. Should return: `{"status": "healthy"}`

3. Visit: `https://YOUR-BACKEND.onrender.com/docs`
4. Should show API documentation

### Test Frontend

1. Visit your Vercel URL: `https://YOUR-APP.vercel.app`
2. You should see your landing page
3. Click **"Login"** or **"Get Started"**
4. Login with:
   - Username: `admin`
   - Password: `admin123`

### Test Full Integration

1. After logging in, try:
   - Upload a document
   - Ask a question in the chat
   - Check if data persists (refresh page)

---

## Part 5: Update CORS (If Needed)

If you get CORS errors, update your backend CORS settings:

### In `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5000",
        "http://localhost:3000",
        "https://YOUR-APP.vercel.app",  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then commit and push:
```bash
git add .
git commit -m "Update CORS for production"
git push
```

Render will auto-deploy the changes!

---

## 🎉 Deployment Complete!

### Your Live URLs:

- **Backend API**: `https://enterprise-rag-backend.onrender.com`
- **Frontend App**: `https://enterprise-rag-xxx.vercel.app`
- **Database**: Neon PostgreSQL (already configured)

### Default Login:
- **Username**: `admin`
- **Password**: `admin123`

---

## 📊 Monitoring & Logs

### Render (Backend):
- Dashboard: https://dashboard.render.com
- Click your service → **"Logs"** tab
- View real-time logs

### Vercel (Frontend):
- Dashboard: https://vercel.com/dashboard
- Click your project → **"Deployments"**
- View deployment logs

### Neon (Database):
- Dashboard: https://console.neon.tech
- View database tables and data

---

## 🔄 Continuous Deployment

Both Render and Vercel are now connected to your GitHub repository!

**To deploy updates:**
1. Make changes to your code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push
   ```
3. **Automatic deployment!**
   - Render will rebuild backend
   - Vercel will rebuild frontend

---

## ⚠️ Important Notes

### Free Tier Limitations:

**Render Free Tier:**
- ✅ 750 hours/month (enough for 1 service)
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ First request after spin-down takes ~30 seconds
- ✅ Auto-deploys on git push

**Vercel Free Tier:**
- ✅ 100 GB bandwidth/month
- ✅ Always online (no spin-down)
- ✅ Auto-deploys on git push
- ✅ Custom domains supported

**Neon Free Tier:**
- ✅ 0.5 GB storage
- ✅ Always online
- ✅ No spin-down

### Keep Render Awake (Optional):

To prevent Render from spinning down, use a service like:
- **UptimeRobot**: https://uptimerobot.com (free)
- Ping your backend every 10 minutes

---

## 🆘 Troubleshooting

### Backend won't start:
1. Check Render logs for errors
2. Verify all environment variables are set
3. Check `requirements.txt` is correct

### Frontend can't connect to backend:
1. Verify `VITE_API_URL` is correct in Vercel
2. Check CORS settings in backend
3. Test backend URL directly in browser

### Database connection failed:
1. Verify `DATABASE_URL` in Render
2. Check Neon database is active
3. Test connection from Render logs

### 404 errors on frontend routes:
1. Verify `vercel.json` is in frontend folder
2. Check rewrites configuration

---

## 🎯 Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Vercel
3. ✅ Test the application
4. 🔄 Set up custom domain (optional)
5. 📊 Monitor usage and logs
6. 🚀 Share your app with users!

---

## Need Help?

If you encounter any issues:
1. Check the logs (Render/Vercel dashboards)
2. Verify all environment variables
3. Test each component separately
4. Ask for help with specific error messages

**Good luck with your deployment!** 🚀
