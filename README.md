# 🤖 Logiq - Discord Bot

AI-Enhanced Discord Bot for Community Management, built with discord.py

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment

Create `.env` file:
```env
DISCORD_BOT_TOKEN=your_discord_bot_token
MONGODB_URI=mongodb://localhost:27017
ENVIRONMENT=development
```

### 3. Run Bot
```bash
python main.py
```

---

## 📦 Features

- ✅ **Verification** - Button/CAPTCHA verification system
- ✅ **Moderation** - Warn, kick, ban, timeout, auto-moderation
- ✅ **Roles** - Self-assignable role menus
- ✅ **Leveling** - XP system with rank cards
- ✅ **Economy** - Virtual currency, daily rewards, gambling
- ✅ **Utility** - Polls, reminders, server stats
- ✅ **Tickets** - Support ticket system
- ✅ **Analytics** - Server activity tracking
- ✅ **Games** - Trivia, dice, roulette, 8ball
- ✅ **Admin** - Bot management commands
- ⭕ **AI Chat** - Optional, requires OpenAI API key

---

## 🗄️ Database Setup

### Option 1: Local MongoDB

**Windows:**
Download from https://www.mongodb.com/try/download/community

**macOS:**
```bash
brew install mongodb-community
brew services start mongodb-community
```

**Linux:**
```bash
sudo apt install mongodb
sudo systemctl start mongodb
```

### Option 2: MongoDB Atlas (Cloud)

1. Sign up at https://www.mongodb.com/cloud/atlas
2. Create free cluster
3. Get connection string
4. Update `.env`:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/logiq
```

---

## 🚂 Deploy to Railway

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/logiq.git
git push -u origin main
```

### 2. Deploy to Railway

1. Go to https://railway.app
2. Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add MongoDB plugin: Click "New" → "Database" → "MongoDB"
6. Add environment variables:
```
DISCORD_BOT_TOKEN=your_token
MONGODB_URI=${{MongoDB.MONGO_URL}}
ENVIRONMENT=production
```
7. Deploy!

### 3. Check Logs

You should see:
```
[INFO] Starting Logiq...
[INFO] Database connected successfully
[INFO] Loading 11 cogs...
[INFO] Bot is ready!
```

---

## 🎮 Commands

### Verification
- `/setup-verification` - Configure verification
- `/send-verification` - Send verification message

### Moderation
- `/warn <user> <reason>` - Warn user
- `/warnings <user>` - View warnings
- `/timeout <user> <duration> <reason>` - Timeout user
- `/kick <user> <reason>` - Kick user
- `/ban <user> <reason>` - Ban user
- `/unban <user_id>` - Unban user
- `/purge <amount>` - Delete messages

### Roles
- `/role-menu <roles>` - Create role menu
- `/addrole <user> <role>` - Add role
- `/removerole <user> <role>` - Remove role
- `/roleinfo <role>` - Role information

### Leveling
- `/rank [user]` - View rank card
- `/leaderboard` - View leaderboard
- `/setlevel <user> <level>` - Set level (admin)

### Economy
- `/balance [user]` - Check balance
- `/daily` - Claim daily reward
- `/give <user> <amount>` - Give currency
- `/coinflip <amount> <choice>` - Flip coin
- `/shop` - View shop

### Utility
- `/poll <question> <options>` - Create poll
- `/remind <duration> <message>` - Set reminder
- `/serverstats` - Server statistics
- `/userinfo [user]` - User information
- `/avatar [user]` - Get avatar

### Tickets
- `/ticket-setup <category> [role]` - Setup tickets
- `/ticket-panel` - Send ticket panel
- `/close-ticket [reason]` - Close ticket

### Analytics
- `/analytics [days]` - View analytics
- `/activity` - Recent activity

### Games
- `/trivia` - Play trivia
- `/roulette <bet> <choice>` - Play roulette
- `/dice [sides]` - Roll dice
- `/8ball <question>` - Magic 8-ball

### Admin
- `/botinfo` - Bot information
- `/config` - View configuration
- `/modules` - Module status
- `/reload <cog>` - Reload cog
- `/sync` - Sync commands
- `/setlogchannel <channel>` - Set log channel

---

## ⚙️ Configuration

Edit `config.yaml` to customize:

```yaml
modules:
  verification:
    enabled: true
  moderation:
    enabled: true
  leveling:
    xp_per_message: 10
    xp_cooldown: 60
  economy:
    currency_name: "Coins"
    currency_symbol: "💎"
    starting_balance: 1000
    daily_reward: 100
  # ... more settings
```

---

## 🔧 Enable AI Features (Optional)

1. Get OpenAI API key from https://platform.openai.com
2. Add to `.env`:
```env
OPENAI_API_KEY=sk-your-key-here
```
3. Enable in `config.yaml`:
```yaml
ai_chat:
  enabled: true
```
4. Use commands:
   - `/ask <question>` - Ask AI
   - `/summarize [count]` - Summarize messages

---

## 🐛 Troubleshooting

### Bot Not Starting

**Check Python version:**
```bash
python --version  # Should be 3.11+
```

**Check environment variables:**
```bash
cat .env  # Make sure DISCORD_BOT_TOKEN is set
```

### Commands Not Showing

1. Run `/sync` command
2. Wait 1 hour for global sync
3. Restart Discord app
4. Check bot permissions

### Database Connection Error

**Check MongoDB is running:**
```bash
# macOS/Linux
sudo systemctl status mongodb

# Windows
# Check Services app for "MongoDB"
```

**Or use MongoDB Atlas** (cloud)

### Railway Deployment Error

If you see:
```
ImportError: cannot import name '_QUERY_OPTIONS' from 'pymongo.cursor'
```

**This is already fixed!** The requirements.txt has the correct versions:
- motor==3.3.2
- pymongo==4.6.1

Just push to GitHub and Railway will redeploy.

---

## 📊 Web API

When enabled, bot exposes REST API on port 8000:

- `GET /` - API info
- `GET /stats` - Bot statistics
- `GET /guilds` - Guild list
- `GET /guilds/{guild_id}` - Guild details
- `GET /guilds/{guild_id}/leaderboard` - Leaderboard
- `GET /health` - Health check

Access at: `http://localhost:8000`

---

## 🧪 Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

---

## 📁 Project Structure

```
logiq/
├── main.py              # Entry point
├── config.yaml          # Configuration
├── .env                 # Environment variables
├── requirements.txt     # Dependencies
│
├── cogs/               # Feature modules
│   ├── verification.py
│   ├── moderation.py
│   ├── roles.py
│   ├── leveling.py
│   ├── economy.py
│   ├── ai_chat.py
│   ├── utility.py
│   ├── tickets.py
│   ├── analytics.py
│   ├── games.py
│   └── admin.py
│
├── database/           # Database layer
│   ├── db_manager.py
│   └── models.py
│
├── utils/              # Utilities
│   ├── embeds.py
│   ├── logger.py
│   ├── permissions.py
│   ├── converters.py
│   └── constants.py
│
├── web/                # REST API
│   └── api.py
│
└── tests/              # Unit tests
    ├── test_database.py
    └── test_utils.py
```

---

## 🔒 Security

- Never commit `.env` file
- Use environment variables for secrets
- Keep bot token private
- Enable 2FA on Discord account
- Regular dependency updates

---

## 📝 License

MIT License - see LICENSE file

---

## 💬 Support

- **Issues**: GitHub Issues
- **Discord**: Bot commands help with `/help`

---

**Made with ❤️ using discord.py**
