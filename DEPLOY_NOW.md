# 🚀 DEPLOYMENT: Step-by-Step Instructions

## ✅ STEP 1: Deploy Backend to Render (10 minutes)

### 1.1 Open Render Dashboard
- Go to: **https://dashboard.render.com**
- Sign in with GitHub (or create account)

### 1.2 Create New Web Service
- Click **"New +"** button (top right)
- Select **"Web Service"**

### 1.3 Connect GitHub Repository
- If first time: Click **"Connect account"** → Authorize Render
- Find repository: **"RagAssistant"** (or your repo name)
- Click **"Connect"**

### 1.4 Configure Service Settings

Fill in these EXACT values:

| Setting | Value |
|---------|-------|
| **Name** | `enterprise-rag-backend` |
| **Region** | `Oregon` (or closest to you) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

### 1.5 Add Environment Variables

Scroll down to **"Environment Variables"** and click **"Add Environment Variable"** for each:

**Variable 1:**
- Key: `DATABASE_URL`
- Value: `postgresql://neondb_owner:npg_w7SB1leAuJMD@ep-steep-firefly-a4s5jaq7-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require`

**Variable 2:**
- Key: `GOOGLE_API_KEY`
- Value: `AIzaSyA5LG2SfjCFpRmOTKPLYyDlyNCResU8nRI`

**Variable 3:**
- Key: `PINECONE_API_KEY`
- Value: `pcsk_6zKudz_7pyfxdHWrt3sjRQb1hD8ZmSJN7w31Cj2hEMoVTXxmc4ZwEqyZ3TCzE9Uw6WoWEd`

**Variable 4:**
- Key: `SESSION_SECRET`
- Value: `super-secret-key-enterprise-rag-2024`

**Variable 5:**
- Key: `PYTHON_VERSION`
- Value: `3.11.0`

### 1.6 Deploy!
- Click **"Create Web Service"** (bottom of page)
- Wait 5-10 minutes for deployment
- Watch the logs - should see: "Default admin user created"

### 1.7 Get Your Backend URL
- After deployment, you'll see: `https://enterprise-rag-backend.onrender.com`
- **COPY THIS URL!** You need it for Vercel
- Test it: Visit `https://enterprise-rag-backend.onrender.com/health`
- Should show: `{"status":"healthy"}`

---

## ✅ STEP 2: Deploy Frontend to Vercel (5 minutes)

### 2.1 Open Vercel Dashboard
- Go to: **https://vercel.com**
- Click **"Sign Up"** or **"Log In"**
- Sign in with GitHub

### 2.2 Import Project
- Click **"Add New..."** → **"Project"**
- Find repository: **"RagAssistant"**
- Click **"Import"**

### 2.3 Configure Project Settings

| Setting | Value |
|---------|-------|
| **Framework Preset** | `Vite` (auto-detected) |
| **Root Directory** | Click "Edit" → Select `frontend` |
| **Build Command** | `npm run build` (auto-filled) |
| **Output Directory** | `dist` (auto-filled) |
| **Install Command** | `npm install` (auto-filled) |

### 2.4 Add Environment Variable

Click **"Environment Variables"** section:

- **Name**: `VITE_API_URL`
- **Value**: `https://enterprise-rag-backend.onrender.com/api/v1`

**⚠️ IMPORTANT**: Replace `enterprise-rag-backend` with YOUR actual Render service name!

### 2.5 Deploy!
- Click **"Deploy"**
- Wait 2-3 minutes
- Vercel will build and deploy

### 2.6 Get Your Frontend URL
- After deployment: `https://rag-assistant-xxx.vercel.app`
- Click **"Visit"** to open your app!

---

## ✅ STEP 3: Test Your Deployed App (2 minutes)

### 3.1 Test Backend
1. Visit: `https://YOUR-BACKEND.onrender.com/health`
2. Should return: `{"status":"healthy"}`
3. Visit: `https://YOUR-BACKEND.onrender.com/docs`
4. Should show API documentation

### 3.2 Test Frontend
1. Visit your Vercel URL
2. Should see your landing page
3. Click **"Login"** or **"Get Started"**

### 3.3 Test Login
- Username: `admin`
- Password: `admin123`
- Should successfully log in!

### 3.4 Test Features
- Upload a document
- Ask a question in chat
- Check if everything works!

---

## 🎉 DEPLOYMENT COMPLETE!

### Your Live Application:

**Backend API**: `https://enterprise-rag-backend.onrender.com`  
**Frontend App**: `https://rag-assistant-xxx.vercel.app`  
**Database**: Neon PostgreSQL (already configured)

### Admin Login:
- Username: `admin`
- Password: `admin123`

---

## 📝 What Happens Next?

### Automatic Deployments:
Every time you push to GitHub:
- ✅ Render automatically redeploys backend
- ✅ Vercel automatically redeploys frontend

### To Update Your App:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

That's it! Both platforms will auto-deploy! 🚀

---

## ⚠️ Important Notes

### Render Free Tier:
- Spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- This is normal for free tier!

### If Backend is Slow:
- First request wakes up the server (30 seconds)
- Subsequent requests are fast
- Consider upgrading to paid tier ($7/month) for always-on

---

## 🆘 Troubleshooting

### "Cannot connect to backend"
1. Check Render logs for errors
2. Verify all environment variables in Render
3. Test backend URL directly

### "CORS error"
1. Backend needs to allow your Vercel URL
2. Will help you fix this if needed

### "Database error"
1. Verify DATABASE_URL in Render
2. Check Neon dashboard - database should be active

---

## 🎯 Next Steps After Deployment

1. ✅ Share your app URL with users
2. 📊 Monitor usage in Render/Vercel dashboards
3. 🔐 Change admin password in production
4. 🌐 Add custom domain (optional)
5. 📈 Upgrade to paid tier when needed

---

**Need help? Check the logs in Render/Vercel dashboards!**

**Ready to deploy? Start with STEP 1!** 🚀
