# 🚀 ISODROP - Vercel Deployment Guide

## ⚠️ Important: Vercel Deployment Limitations

**Vercel is optimized for serverless functions, which have limitations for ISODROP:**

1. **No WebSocket Support** - Real-time SocketIO won't work on Vercel
2. **Function Timeout** - 10-60 seconds max execution time
3. **Memory Constraints** - 512MB memory per function
4. **No Persistent Connections** - State is lost between requests
5. **File Size Limit** - 50MB max (ISODROP needs up to 5GB)

---

## ✅ What Works on Vercel

- REST API endpoints for messaging
- File upload (limited to 50MB)
- Device registration
- Server info & QR code generation
- Basic functionality without real-time features

---

## 🚀 Deploy to Vercel (If You Must)

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Deploy

```bash
vercel deploy --prod
```

### Step 4: Access Your App

Your app will be available at: `https://[project-name].vercel.app`

---

## ❌ Better Alternatives (Recommended)

### **Option 1: Render (BEST FOR FULL EXPERIENCE)**

Render supports Flask-SocketIO perfectly and has a free tier.

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Choose Python environment
5. Set start command: `python app.py`
6. Deploy!

**Advantages:**
- ✅ Full WebSocket support
- ✅ 5GB file support
- ✅ Real-time messaging works
- ✅ Free tier available
- ✅ Auto-restart on error

### **Option 2: Railway**

Railway is beginner-friendly with automatic deployment.

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Connect your repository
5. Auto-detects Python & starts

**Advantages:**
- ✅ Easy setup (no config needed)
- ✅ Full SocketIO support
- ✅ $5 monthly free credit
- ✅ Automatic scaling
- ✅ Great documentation

### **Option 3: Heroku Alternative (Railway/Render)**

Heroku discontinued free tiers, but alternatives offer better value:

1. Use Railway or Render
2. Both have free tier options
3. Both fully support Python Flask

---

## 📝 Recommended: Deploy on Render

### Complete Step-by-Step:

1. **Create GitHub Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial ISODROP commit"
   git remote add origin https://github.com/YOUR_USERNAME/isodrop.git
   git push -u origin main
   ```

2. **Go to Render.com:**
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Select your repository
   - Choose branch: `main`

3. **Configure Settings:**
   - **Name:** `isodrop`
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`

4. **Environment Variables:**
   - Set `FLASK_ENV` = `production`

5. **Click Deploy!**

6. **Access Your App:**
   - Your URL: `https://isodrop.onrender.com`
   - Share QR code or URL with others

---

## 🐳 Docker Deployment (Advanced)

If you want to use containers:

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY index.html .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Deploy to Railway/Render with Docker:

1. Render automatically detects Dockerfile
2. Railway supports Docker natively
3. No additional configuration needed

---

## 🔒 Environment Variables for Vercel

If you deploy to Vercel, set these environment variables:

```
FLASK_ENV=production
VERCEL_URL=your-domain.vercel.app
MAX_FILE_SIZE=52428800  # 50MB for Vercel
```

---

## ⚡ Quick Comparison

| Platform | WebSocket | File Size | Free Tier | Recommended |
|----------|-----------|-----------|-----------|-------------|
| **Vercel** | ❌ No | 50MB | ✅ Yes | ❌ Poor for ISODROP |
| **Render** | ✅ Yes | 5GB+ | ✅ Yes | ✅✅ BEST |
| **Railway** | ✅ Yes | 5GB+ | ✅ Yes | ✅✅ BEST |
| **Heroku** | ✅ Yes | Unlimited | ❌ No | ❌ Too Expensive |

---

## 🎯 My Recommendation

**Use Railway or Render (NOT Vercel) for ISODROP:**

### Why?
1. Full real-time WebSocket support
2. Up to 5GB file transfers
3. Free tier or cheap paid tiers
4. Better suited for Flask apps
5. Easier deployment process
6. More reliable for production

### Quick Start with Railway:

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub
3. Done! Auto-deploys with each push

---

## 📞 Files Included for Vercel

If you still want to deploy on Vercel:

- `vercel.json` - Configuration
- `api/index.py` - Serverless function
- `api/requirements.txt` - Dependencies
- `.vercelignore` - Ignore files

But **strongly recommend Render or Railway** for best ISODROP experience.

---

## 🔗 Deployment Links

- **Render:** https://render.com
- **Railway:** https://railway.app
- **Vercel:** https://vercel.com
- **Docker Docs:** https://docs.docker.com

---

**Choose Render or Railway for the best ISODROP experience! 🚀**
