# 🚂 Railway Deployment Guide - ProgrammifyBot

Deploy your Discord bot to Railway in under 10 minutes!

---

## 🌟 Why Railway?

- ✅ **Free Tier** - $5 free credit monthly
- ✅ **Auto Deploy** - Connects to GitHub
- ✅ **Free MongoDB** - Built-in plugin
- ✅ **Easy Setup** - No Docker knowledge needed
- ✅ **24/7 Uptime** - Always online
- ✅ **Logs & Monitoring** - Built-in dashboard

---

## 📋 Prerequisites

- ✅ GitHub account
- ✅ Railway account (free)
- ✅ Discord bot token
- ✅ Project code ready

---

## 🚀 Step-by-Step Deployment

### Step 1: Push Code to GitHub

```bash
# Initialize git (if not already done)
cd programmifybot
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - ProgrammifyBot"

# Create GitHub repo and push
# Go to github.com and create new repository
git remote add origin https://github.com/YOUR_USERNAME/programmifybot.git
git branch -M main
git push -u origin main
```

### Step 2: Sign Up for Railway

1. Go to https://railway.app
2. Click "Login" → "Login with GitHub"
3. Authorize Railway

### Step 3: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `programmifybot` repository
4. Click "Deploy Now"

### Step 4: Add MongoDB

1. In your Railway project dashboard
2. Click "New" → "Database" → "Add MongoDB"
3. MongoDB will be automatically created
4. Connection string is auto-configured

### Step 5: Configure Environment Variables

1. Click on your bot service
2. Go to "Variables" tab
3. Add these variables:

```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
MONGODB_URI=${{MongoDB.MONGO_URL}}
ENVIRONMENT=production
```

**Note:** `${{MongoDB.MONGO_URL}}` automatically references the MongoDB connection

### Step 6: Configure Start Command

1. In your service settings
2. Go to "Settings" → "Deploy"
3. Set **Start Command**:
```
python main.py
```

### Step 7: Deploy!

1. Click "Deploy"
2. Wait for deployment (1-2 minutes)
3. Check logs to confirm bot is online

---

## 📊 Verify Deployment

### Check Logs

1. Go to your service in Railway
2. Click "Deployments"
3. Click latest deployment
4. View logs - you should see:
```
[INFO] Starting ProgrammifyBot...
[INFO] Database connected successfully
[INFO] Loading 11 cogs...
[INFO] Bot is ready!
```

### Check Bot Status

In Discord:
- Bot should show as "Online"
- Try `/botinfo` command

---

## 🔧 Project Files for Railway

Railway needs these files (already included):

### 1. **requirements.txt** ✅
Already created - lists all dependencies

### 2. **main.py** ✅
Entry point - already configured

### 3. **.gitignore** ✅
Prevents uploading secrets

---

## 💰 Railway Pricing

**Free Tier:**
- $5 credit per month
- ~500 hours runtime
- Perfect for small bots
- No credit card required initially

**If you need more:**
- $5/month for 100 more hours
- Scales automatically

---

## 🔄 Auto-Deploy Updates

Every time you push to GitHub, Railway auto-deploys!

```bash
# Make changes to your code
git add .
git commit -m "Added new feature"
git push

# Railway automatically redeploys! 🎉
```

---

## 📊 Monitoring Your Bot

### View Logs
1. Railway Dashboard → Your Service
2. Click "Deployments"
3. View real-time logs

### Check Metrics
1. Go to "Metrics" tab
2. See CPU, Memory, Network usage

### Check Database
1. Click on MongoDB service
2. View "Metrics" and "Logs"

---

## 🔧 Environment Variables Reference

Required:
```
DISCORD_BOT_TOKEN=your_bot_token
MONGODB_URI=${{MongoDB.MONGO_URL}}
ENVIRONMENT=production
```

Optional (if enabling AI features):
```
OPENAI_API_KEY=your_openai_key
```

---

## 🐛 Troubleshooting

### Bot Not Starting

**Check Logs:**
1. Railway Dashboard → Service → Logs
2. Look for error messages

**Common Issues:**
- Missing `DISCORD_BOT_TOKEN`
- Invalid MongoDB connection
- Missing dependencies in `requirements.txt`

### Database Connection Error

**Check MongoDB:**
1. Make sure MongoDB plugin is added
2. Verify `MONGODB_URI` variable exists
3. Should be: `${{MongoDB.MONGO_URL}}`

### Commands Not Working

**After first deploy:**
1. Wait 5-10 minutes for commands to sync globally
2. Or run `/sync` command in Discord
3. Restart Discord app

### Build Failing

**Check requirements.txt:**
- Make sure all packages are valid
- Railway uses Python 3.11

**View Build Logs:**
- Railway Dashboard → Deployments → Build Logs

---

## 🔒 Security Best Practices

✅ **Never commit `.env` file**
✅ **Use Railway environment variables**
✅ **Keep bot token secret**
✅ **Enable 2FA on Discord**
✅ **Regular updates** - push security patches

---

## 📈 Scaling

### If Bot Grows:

**1. Upgrade Railway Plan**
- More runtime hours
- Better resources

**2. Optimize Code**
- Use caching
- Optimize database queries
- Connection pooling (already implemented)

**3. Monitor Usage**
- Check Railway metrics
- Monitor MongoDB size
- Watch for memory leaks

---

## 🔄 Backup Strategy

### Database Backups

**Option 1: MongoDB Atlas (Recommended)**
Instead of Railway MongoDB:
1. Create free MongoDB Atlas cluster
2. Use Atlas connection string
3. Automatic backups included

**Option 2: Manual Backups**
```bash
# On your local machine
mongodump --uri="your_railway_mongodb_uri" --out=backup_folder
```

---

## 🌐 Custom Domain (Optional)

1. Railway Dashboard → Service
2. Go to "Settings" → "Networking"
3. Click "Generate Domain"
4. Use for API access: `https://your-bot.railway.app`

---

## 💡 Pro Tips

**1. Use Railway CLI** (optional)
```bash
npm install -g @railway/cli
railway login
railway logs
```

**2. Environment Branches**
- Create separate Railway environments
- One for testing, one for production

**3. Monitor Costs**
- Check Railway usage dashboard
- Set up billing alerts

**4. Database Indexing**
- Add indexes for better performance
- Use MongoDB Compass to manage

---

## ✅ Deployment Checklist

Before deploying:

- [ ] Code pushed to GitHub
- [ ] `.env` NOT committed
- [ ] `requirements.txt` complete
- [ ] Discord bot token ready
- [ ] Railway account created
- [ ] MongoDB plugin added
- [ ] Environment variables set
- [ ] Start command configured
- [ ] Bot tested locally first

After deploying:

- [ ] Check logs for errors
- [ ] Verify bot is online in Discord
- [ ] Run `/sync` command
- [ ] Test key features
- [ ] Monitor for 24 hours
- [ ] Set up alerts (optional)

---

## 📞 Need Help?

**Railway Support:**
- Documentation: https://docs.railway.app
- Discord: https://discord.gg/railway
- GitHub: https://github.com/railwayapp

**Bot Issues:**
- Check Railway logs first
- Review `logs/bot.log` (if logging to file)
- GitHub Issues for code problems

---

## 🎉 You're Live!

Your bot is now:
- ✅ Running 24/7
- ✅ Auto-deploying updates
- ✅ Backed by Railway infrastructure
- ✅ Monitored and logged

**Next Steps:**
1. Invite bot to your Discord server
2. Run `/sync` to register commands
3. Configure modules with setup commands
4. Monitor usage and performance
5. Push updates as needed

---

**Railway Dashboard:** https://railway.app/dashboard

**Happy Hosting! 🚂**
