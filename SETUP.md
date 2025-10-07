# 🤖 Logiq Setup Guide

Simple MEE6-style Discord bot with essential features only.

---

## ✅ What's Included

- ✅ **Verification System** - Button/CAPTCHA verification
- ✅ **Moderation Tools** - Warn, kick, ban, timeout, mute
- ✅ **Role Management** - Self-assignable role menus
- ✅ **Leveling System** - XP and rank cards
- ✅ **Economy** - Virtual currency, daily rewards, gambling
- ✅ **Utility** - Polls, reminders, server stats
- ✅ **Tickets** - Support ticket system
- ✅ **Analytics** - Server activity tracking
- ✅ **Games** - Trivia, dice, roulette, 8ball
- ✅ **Admin Panel** - Bot management commands

**Note:** AI chat and music features are disabled by default (optional add-ons).

---

## 🚀 Installation

### Step 1: Install Python

Download and install **Python 3.11 or higher**:
- Windows: https://www.python.org/downloads/
- Check "Add Python to PATH" during installation

Verify installation:
```bash
python --version
```

### Step 2: Get Bot Token

1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Go to "Bot" tab
4. Click "Reset Token" and copy it
5. Enable these **Privileged Gateway Intents**:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent

### Step 3: Setup Bot

```bash
# Navigate to bot directory
cd Logiq

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure

Create `.env` file:
```env
DISCORD_BOT_TOKEN=your_bot_token_here
MONGODB_URI=mongodb://localhost:27017
ENVIRONMENT=development
```

**That's it!** No API keys needed for basic features.

---

## 🗄️ Database Setup

### Option 1: Local MongoDB (Easy)

**Windows:**
1. Download MongoDB Community: https://www.mongodb.com/try/download/community
2. Install with default settings
3. MongoDB starts automatically
4. Use: `MONGODB_URI=mongodb://localhost:27017`

**macOS:**
```bash
brew install mongodb-community
brew services start mongodb-community
```

**Linux:**
```bash
sudo apt install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### Option 2: MongoDB Atlas (Cloud - Free)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create free cluster (M0)
4. Create database user
5. Whitelist all IPs: `0.0.0.0/0`
6. Get connection string
7. Update `.env`:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/Logiq
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

## 🎮 Invite Bot to Server

Replace `YOUR_BOT_ID` with your bot's Client ID:

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=8&scope=bot%20applications.commands
```

**Permissions Needed:**
- Administrator (or manually select: Manage Roles, Kick, Ban, Manage Channels, etc.)

---

## 🔧 Initial Setup Commands

Run these in your Discord server:

### 1. Sync Commands
```
/sync
```
*Wait a few minutes for commands to appear*

### 2. Setup Moderation Logs
```
/setlogchannel channel:#mod-logs
```

### 3. Setup Verification
```
/setup-verification channel:#verify role:@Verified verification_type:button
/send-verification
```

### 4. Create Role Menu
```
/role-menu roles:@Gaming @Music @Art
```

### 5. Setup Support Tickets
```
/ticket-setup category:Support support_role:@Support
/ticket-panel
```

---

## 📝 Essential Commands

### Moderation
- `/warn @user reason` - Warn a user
- `/warnings @user` - View warnings
- `/timeout @user 1h reason` - Timeout for 1 hour
- `/kick @user reason` - Kick user
- `/ban @user reason` - Ban user
- `/purge 50` - Delete 50 messages

### Leveling
- `/rank` - View your rank
- `/leaderboard` - Top 10 users

### Economy
- `/balance` - Check balance
- `/daily` - Claim daily reward
- `/give @user 500` - Give coins
- `/coinflip 100 heads` - Gamble

### Utility
- `/poll "Question?" "Option1" "Option2"` - Create poll
- `/remind 30m Take a break` - Set reminder
- `/serverstats` - Server info
- `/userinfo @user` - User info

### Games
- `/trivia` - Play trivia
- `/dice` - Roll dice
- `/8ball Will it rain?` - Magic 8-ball

### Admin
- `/botinfo` - Bot statistics
- `/config` - View configuration
- `/modules` - Module status
- `/reload cog_name` - Reload cog

---

## 🎨 Customization

### Edit XP Rates

Edit `config.yaml`:
```yaml
leveling:
  enabled: true
  xp_per_message: 15    # Change this
  xp_cooldown: 60
```

### Edit Currency Settings

```yaml
economy:
  enabled: true
  currency_name: "Coins"  # Change this
  currency_symbol: "🪙"    # Change this
  starting_balance: 500   # Change this
  daily_reward: 50        # Change this
```

### Enable/Disable Modules

```yaml
modules:
  verification:
    enabled: true   # Set to false to disable
  leveling:
    enabled: true
  economy:
    enabled: true
  # etc...
```

---

## 🆘 Troubleshooting

### Commands Not Showing

1. Run `/sync` command
2. Wait 1 hour for global sync
3. Restart Discord app
4. Check bot has `applications.commands` scope

### Database Connection Error

**Check MongoDB is running:**
```bash
# Windows - check Services app for "MongoDB"
# macOS/Linux:
sudo systemctl status mongodb
```

**Or use MongoDB Atlas** (cloud option above)

### Bot Not Responding

1. Check bot is online in Discord
2. Check console for errors
3. Verify bot has proper permissions
4. Make sure intents are enabled in Developer Portal

### Module Not Working

Check in `config.yaml` that module is enabled:
```yaml
modules:
  module_name:
    enabled: true  # Must be true
```

---

## 📊 Web Dashboard (Optional)

Access bot stats at: `http://localhost:8000`

**Endpoints:**
- `/stats` - Bot statistics
- `/guilds` - Server list
- `/guilds/GUILD_ID/leaderboard` - Server leaderboard
- `/health` - Health check

---

## 🔄 Updating the Bot

```bash
git pull
pip install -r requirements.txt
python main.py
```

---

## 📦 Optional Features

### Enable AI Chat

1. Get OpenAI API key: https://platform.openai.com/api-keys
2. Add to `.env`:
```env
OPENAI_API_KEY=sk-your-key-here
```
3. Enable in `config.yaml`:
```yaml
ai_chat:
  enabled: true
```
4. Restart bot
5. Use `/ask` command

### Enable Music (Advanced)

1. Install FFmpeg
2. Install additional packages:
```bash
pip install yt-dlp pynacl
```
3. Enable in config
4. Implement voice client (see music.py)

---

## 🎯 Tips

- **Use different channels** for different features (verify, logs, tickets)
- **Set up role hierarchy** properly (bot role above managed roles)
- **Regular backups** of MongoDB database
- **Monitor logs** in `logs/bot.log`
- **Test commands** in a test server first

---

## 📞 Need Help?

- **Check logs**: `logs/bot.log`
- **Common issues**: See troubleshooting above
- **GitHub Issues**: Report bugs
- **Documentation**: See README.md

---

**You're all set! Enjoy your new Discord bot! 🎉**
