# 🚀 ISODROP - Railway.app Deployment (RECOMMENDED)

## ✅ Why Railway is Perfect for ISODROP

- ✅ Full WebSocket/SocketIO support
- ✅ Supports 5GB+ file transfers
- ✅ Free tier with $5 monthly credit
- ✅ Auto-deploy from GitHub
- ✅ Zero configuration needed
- ✅ Perfect for Flask + SocketIO
- ✅ Automatic scaling
- ✅ Great documentation

---

## 🚀 Deploy to Railway in 5 Minutes

### Step 1: Prepare Your Repository

```bash
cd C:\Users\praka\Desktop\wifi

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial ISODROP commit"

# Create repo on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/isodrop.git
git push -u origin main
```

### Step 2: Sign Up on Railway

1. Go to **[railway.app](https://railway.app)**
2. Click **"Start Project"**
3. Click **"Deploy from GitHub repo"**
4. Authorize Railway to access GitHub
5. Select your `isodrop` repository

### Step 3: Configure Project

Railway auto-detects Python! Just:

1. Click **"Deploy Now"**
2. Wait for deployment (2-3 minutes)
3. Your app is live! 🎉

### Step 4: Get Your URL

After deployment:

1. Open your Railway dashboard
2. Click on your project
3. Copy the URL from "Domains" section
4. URL format: `https://isodrop-[random].railway.app`

---

## 🎯 Manual Configuration (If Needed)

### Environment Variables

If auto-detection doesn't work, set:

1. **Start Command:**
   ```
   python app.py
   ```

2. **Port:**
   ```
   5000
   ```

3. **Environment Variables:**
   - `FLASK_ENV` = `production`
   - `PORT` = `5000`

### Procfile (Optional)

Create `Procfile` in project root:

```
web: python app.py
```

---

## 🌐 Share Your ISODROP Instance

Once deployed:

1. **Get your URL:** https://isodrop-[random].railway.app
2. **Share with others on internet** ✅
3. **QR code works** - scan to join
4. **Real-time messaging works** ✅
5. **File sharing works** ✅ (up to 5GB)

---

## 📊 Railway Dashboard

Monitor your app:

1. **Logs** - See what's happening
2. **Metrics** - CPU, Memory, Network
3. **Deployments** - History of deploys
4. **Variables** - Change settings without redeploy

---

## 💡 Tips & Tricks

### Auto-redeploy on Push

Once set up, every push to GitHub automatically:
1. Triggers new deployment
2. App updates in ~2 minutes
3. No manual intervention needed

### View Live Logs

```bash
# In Railway Dashboard, click "Logs" tab
# See real-time activity
```

### Scale Your App

Railway automatically scales based on traffic. You can also:

1. Go to settings
2. Increase memory allocation
3. Add more resources as needed

### Custom Domain

1. Go to project settings
2. Add custom domain
3. Update DNS records (Railway provides instructions)

---

## 🔒 Security & Environment

### Protect with PIN (Optional)

Edit `app.py` to add PIN protection:

```python
PIN_CODE = "1234"  # Change this
```

### Enable HTTPS

Railway automatically provides HTTPS for all deployments! 🔒

---

## 📈 Scale from Local to Cloud

### Local (Development)
```bash
python app.py
# http://localhost:5000
```

### Railway (Production)
```
https://isodrop-[random].railway.app
# Automatic HTTPS
# Real WebSocket support
# 5GB files work perfectly
```

---

## 🆘 Troubleshooting

### Build Failed
1. Check `requirements.txt` exists
2. Ensure Python syntax is correct
3. View logs in Railway dashboard

### App Not Starting
1. Check "Start Command" is `python app.py`
2. Verify `PORT` is set to 5000
3. Check logs for error messages

### Files Not Persisting
This is normal! Railway is stateless. Files clear on redeploy.
- Use database for persistence (optional)
- Or keep sessions short

### WebSocket Not Working
- Verify Railway shows "healthy"
- Check browser console for errors
- Try different browser
- Ensure using HTTPS URL

---

## 💾 Backup & Restore

### Export Data

```bash
# Before deleting project
# Download logs and files
# From Railway dashboard → Export
```

### Switch Between Branches

Railway can deploy different branches:

1. Go to project settings
2. Change "Deploy Branch" to `staging` or `dev`
3. Auto-deploys from new branch

---

## 🎓 Next Steps After Deployment

### 1. Test Everything
- [ ] Send messages
- [ ] Upload file
- [ ] Preview image
- [ ] Download file
- [ ] Check QR code

### 2. Share & Invite
- [ ] Get URL
- [ ] Share with team
- [ ] Test from mobile

### 3. Customize (Optional)
- [ ] Change colors in HTML
- [ ] Add PIN protection
- [ ] Modify file size limits

### 4. Monitor
- [ ] Watch logs in Railway
- [ ] Check performance metrics
- [ ] Monitor usage

---

## 📚 Useful Links

- **Railway Docs:** https://docs.railway.app
- **Flask SocketIO:** https://python-socketio.readthedocs.io
- **GitHub:** https://github.com
- **Python:** https://python.org

---

## ✨ Success Checklist

- [ ] GitHub repo created
- [ ] Signed up on railway.app
- [ ] Project deployed successfully
- [ ] Green "healthy" indicator in dashboard
- [ ] Can access https://isodrop-[random].railway.app
- [ ] QR code appears
- [ ] Messages sync in real-time
- [ ] File upload works
- [ ] Video playback works

---

## 🎉 Congratulations!

You now have ISODROP running on Railway with:

✅ Real-time messaging  
✅ File sharing (up to 5GB)  
✅ Beautiful dark UI  
✅ Mobile responsive  
✅ HTTPS secured  
✅ Auto-scaling  
✅ Production-ready  

**Share the URL and start collaborating! 🚀**

---

## 📞 Need Help?

1. Check [Railway Docs](https://docs.railway.app)
2. See [DEPLOYMENT.md](DEPLOYMENT.md) for general tips
3. Review [README.md](README.md) for features
4. Check error logs in Railway dashboard

---

**Railway is the perfect choice for ISODROP!** 🌟
