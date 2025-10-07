# ⚡ Logiq Quick Start Guide

Get Logiq up and running in 5 minutes!

---

## 🎯 Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Discord Bot Token ([Get one here](https://discord.com/developers/applications))
- [ ] MongoDB installed locally OR MongoDB Atlas account
- [ ] (Optional) OpenAI API Key for AI features

---

## 🚀 Installation (3 Steps)

### Step 1: Get the Code

```bash
git clone https://github.com/yourusername/Logiq.git
cd Logiq
```

### Step 2: Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your values
# Required: DISCORD_BOT_TOKEN, MONGODB_URI
# Optional: OPENAI_API_KEY
```

**Minimal `.env` file:**
```env
DISCORD_BOT_TOKEN=your_bot_token_here
MONGODB_URI=mongodb://localhost:27017
```

---

## ▶️ Run the Bot

```bash
python main.py
```

You should see:
```
[INFO] Starting Logiq...
[INFO] Database connected successfully
[INFO] Loading 12 cogs...
[INFO] Bot is ready!
```

---

## 🎮 First Commands

### 1. Invite Bot to Server

Use this URL (replace `YOUR_BOT_ID`):
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=8&scope=bot%20applications.commands
```

### 2. Sync Commands

In Discord, type:
```
/sync
```

### 3. Try These Commands

```
/botinfo          # View bot information
/serverstats      # See server statistics
/ask What is Python?    # Ask AI a question (if OpenAI key configured)
/coinflip 100 heads     # Play coinflip
/poll "Pizza or Burger?" "Pizza" "Burger"   # Create a poll
```

---

## 🔧 Basic Configuration

### Setup Verification

```
/setup-verification channel:#verify role:@Verified verification_type:button
/send-verification
```

### Setup Moderation Logs

```
/setlogchannel channel:#mod-logs
```

### Create Role Menu

```
/role-menu roles:@Role1 @Role2 @Role3
```

### Setup Tickets

```
/ticket-setup category:Support support_role:@Support
/ticket-panel
```

---

## 🐳 Docker Quick Start (Alternative)

If you prefer Docker:

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your values

# 2. Start everything
docker-compose up -d

# 3. View logs
docker-compose logs -f bot

# 4. Stop
docker-compose down
```

---

## 📊 Web Dashboard

If web module is enabled in `config.yaml`:

Visit: `http://localhost:8000`

**Endpoints:**
- `http://localhost:8000/stats` - Bot statistics
- `http://localhost:8000/guilds` - Guild list
- `http://localhost:8000/health` - Health check

---

## ⚙️ Module Configuration

Edit `config.yaml` to enable/disable features:

```yaml
modules:
  verification:
    enabled: true
  moderation:
    enabled: true
  ai_chat:
    enabled: true  # Requires OpenAI key
  economy:
    enabled: true
  leveling:
    enabled: true
  # ... etc
```

---

## 🆘 Troubleshooting

### Bot won't start

**Check Python version:**
```bash
python --version  # Should be 3.11+
```

**Check environment variables:**
```bash
# Make sure .env file exists and has correct values
cat .env
```

### Commands not appearing

1. Wait 1 hour (global sync takes time)
2. Or restart Discord client
3. Or use `/sync` command

### Database connection error

**Check MongoDB is running:**
```bash
# macOS/Linux
sudo systemctl status mongodb

# Windows - check Services app
```

**Or use MongoDB Atlas:**
```env
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/Logiq
```

### AI commands not working

Make sure you have OpenAI API key:
```env
OPENAI_API_KEY=sk-...your-key-here
```

And AI module is enabled in `config.yaml`:
```yaml
modules:
  ai_chat:
    enabled: true
```

---

## 📚 Next Steps

1. **Read Full Documentation**: [README.md](README.md)
2. **Deploy to Production**: [DEPLOYMENT.md](DEPLOYMENT.md)
3. **Customize Settings**: Edit `config.yaml`
4. **Setup Auto-moderation**: Configure in `config.yaml`
5. **Create Custom Shop**: Use database commands
6. **Monitor Analytics**: Use `/analytics` command

---

## 💡 Useful Commands

### Development
```bash
# Run with auto-reload (install watchdog)
pip install watchdog
watchmedo auto-restart -p "*.py" -R python main.py

# Run tests
pytest

# Check code style
flake8 .
```

### Database
```bash
# Connect to MongoDB
mongosh Logiq

# View collections
show collections

# View users
db.users.find()
```

### Docker
```bash
# View logs
docker-compose logs -f

# Restart bot
docker-compose restart bot

# Rebuild after code changes
docker-compose up -d --build
```

---

## 🎉 You're All Set!

Your bot should now be running with all features enabled!

### Join Our Community

- **Issues**: [GitHub Issues](https://github.com/yourusername/Logiq/issues)
- **Discord**: [Support Server](https://discord.gg/your-invite)
- **Docs**: [Full Documentation](README.md)

### Feature Highlights

✅ Verification System
✅ Moderation Tools
✅ XP & Leveling
✅ Virtual Economy
✅ AI Chatbot
✅ Support Tickets
✅ Games & Fun
✅ Analytics
✅ And much more!

---

**Happy Bot Management! 🤖**
