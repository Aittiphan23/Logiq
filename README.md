# 🤖 Logiq - Discord Bot

**Professional Discord Bot for Community Management**

Owned and operated by **Programmify** - All rights reserved.

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

### 🔐 Verification System
- **DM-based verification** - Private verification via DMs
- **No public announcements** - Silent role assignment
- **Custom welcome messages** - Personalized greetings
- **Button or CAPTCHA** - Flexible verification methods

### 🎮 Button-Based Games
- **Dice Roll** - Roll dice with buttons
- **Coinflip** - Heads or tails betting
- **Trivia** - Multiple choice questions
- **8-Ball** - Magic 8-ball predictions
- **Admin Setup** - Deploy game panel with one command

### 🎫 Ticket System
- **Persistent buttons** - Always-available ticket creation
- **User-specific** - Private channels for each user
- **Permission-based** - Only owner/staff can close
- **Auto-managed** - Clean channel creation and deletion

### 🎭 Role Management (FORM-BASED SETUP!)
- **Easy form setup** - Create role menus with a Discord form
- **Custom emojis** - Add emojis to each role option
- **Custom labels** - Name roles however you want
- **Custom title & description** - Fully customizable embed
- **Exclusive roles** - Pick one, others auto-removed
- **Multi-select** - Choose multiple roles
- **Beautiful dropdowns** - User-friendly interface

### 💰 Economy System
- Virtual currency with balance tracking
- Daily rewards and transfers
- Admin balance management

### 📊 Leveling System
- XP on messages
- Rank cards and leaderboards
- Admin level management

### 🛡️ Moderation
- Warn, kick, ban, timeout
- Auto-moderation (spam, mentions)
- Warning tracking

### 🔧 Utility Commands
- Polls with voting buttons
- Reminders
- Server statistics
- User info and avatars

### 📈 Analytics
- Message tracking
- Join/leave analytics
- Activity monitoring

---

## 🗄️ Database Setup

### MongoDB Atlas (Recommended)

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

---

## 🎮 Commands

### 👥 PUBLIC COMMANDS (Users can use)
- `/rank [user]` - View rank card
- `/balance [user]` - Check balance
- `/leaderboard` - View server leaderboard

### 🔧 ADMIN COMMANDS (Administrators only)

#### Verification
- `/setup-verification <role> [type]` - Setup DM verification
- `/set-welcome-message <message>` - Custom welcome DM
- `/send-verification` - Send verification button

#### Tickets
- `/ticket-setup <category> [role]` - Setup ticket system
- `/ticket-panel` - Deploy ticket creation button
- `/close-ticket [reason]` - Close ticket

#### Games
- `/setup-game-panel` - Deploy all game buttons

#### Roles (FORM-BASED!)
- `/create-role-menu` - **Opens a form to create role menu!**
  - Fill in title, description, emojis, and mention roles with @
  - Discord auto-completes role names when you type @
  - Choose exclusive (pick one) or multi-select
  - Automatically creates beautiful dropdown menu for users
- `/addrole <user> <role>` - Add role to user
- `/removerole <user> <role>` - Remove role from user

#### Economy
- `/addbalance <user> <amount>` - Add balance
- `/daily` - Claim daily reward
- `/give <user> <amount>` - Transfer currency
- `/shop` - View shop

#### Leveling
- `/setlevel <user> <level>` - Set user level
- `/resetlevels` - Reset all levels

#### Utility
- `/poll <question> <options>` - Create poll
- `/remind <duration> <message>` - Set reminder
- `/serverstats` - Server statistics
- `/userinfo [user]` - User information
- `/avatar [user]` - Get avatar

#### Analytics
- `/analytics [days]` - View analytics
- `/activity` - Recent activity

#### Admin
- `/botinfo` - Bot information
- `/config` - View configuration
- `/modules` - Module status
- `/reload <cog>` - Reload cog
- `/sync` - Sync commands
- `/setlogchannel <channel>` - Set log channel
- `/purge <amount>` - Delete messages

### 🛡️ MODERATOR COMMANDS
- `/warn <user> <reason>` - Warn user
- `/warnings <user>` - View warnings
- `/timeout <user> <duration>` - Timeout user
- `/kick <user> <reason>` - Kick user
- `/ban <user> <reason>` - Ban user
- `/unban <user_id>` - Unban user

---

## 🎭 How to Create Role Menus (SUPER EASY!)

### Step 1: Run the command
```
/create-role-menu
```

### Step 2: Fill in the form

A Discord form will pop up with the following fields:

**Menu Title:**
```
Choose Your Region
```

**Menu Description:**
```
Select your region from the dropdown below!
```

**Roles (mention with @):**
Simply type `@` and select roles - that's it! The bot will use the role's actual name and emoji.
```
@USA @Europe @Asia @Africa
```
Or one per line:
```
@USA
@Europe
@Asia
@Africa
```

**Exclusive? (yes/no):**
```
yes
```

### Step 3: Submit!

The bot will create a beautiful dropdown menu with the roles' actual names and emojis!

**Tips:**
- Just type `@` and Discord will show you all available roles to pick from
- The bot automatically uses the role's actual emoji (if it has one) or a default 🎭
- The bot automatically uses the role's actual name
- Set "yes" for exclusive if users can only pick ONE role
- Set "no" for multi-select if users can pick multiple roles
- After you submit, a beautiful dropdown menu appears for users to select from!
- Users click the dropdown and see all the roles you added

---

## ⚙️ Configuration

Edit `config.yaml`:

```yaml
database:
  mongodb_uri: "${MONGODB_URI}"
  database_name: "Logiq"

modules:
  verification:
    enabled: true
  moderation:
    enabled: true
  leveling:
    enabled: true
    xp_per_message: 10
    xp_cooldown: 60
  economy:
    enabled: true
    currency_name: "Coins"
    currency_symbol: "💎"
    starting_balance: 1000
    daily_reward: 100

web:
  enabled: true
  port: "${PORT}"
```

---

## 🐛 Troubleshooting

### Bot Not Starting
```bash
python --version  # Ensure Python 3.11+
cat .env          # Check DISCORD_BOT_TOKEN is set
```

### Commands Not Showing
1. Run `/sync` command in Discord
2. Wait 1 hour for global sync
3. Restart Discord app

### Database Connection Error
- Ensure MongoDB URI is correct
- Check MongoDB Atlas IP whitelist (allow all: 0.0.0.0/0)

---

## 📁 Project Structure

```
logiq/
├── main.py              # Entry point
├── config.yaml          # Configuration
├── .env                 # Environment variables
├── requirements.txt     # Dependencies
├── railway.json         # Railway config
├── runtime.txt          # Python version
│
├── cogs/               # Feature modules
│   ├── verification.py  # DM verification
│   ├── moderation.py    # Moderation tools
│   ├── roles.py         # Role management (FORM-BASED!)
│   ├── leveling.py      # XP system
│   ├── economy.py       # Currency system
│   ├── utility.py       # Utility commands
│   ├── tickets.py       # Support tickets
│   ├── analytics.py     # Analytics tracking
│   ├── games.py         # Button-based games
│   └── admin.py         # Bot management
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
└── web/                # API endpoints
    └── api.py
```

---

## 🔒 Security

- Never commit `.env` file
- Keep bot token private
- Use environment variables for secrets
- Regular dependency updates

---

## 📝 License

**PROPRIETARY LICENSE**

Copyright (c) 2025 Programmify. All Rights Reserved.

Logiq is owned and operated by Programmify. No person or entity is granted permission to use, copy, modify, merge, publish, distribute, sublicense, or sell copies of this software without explicit written permission from Programmify.

See LICENSE file for full details.

---

## 💬 Support

For licensing inquiries or support, contact Programmify.

---

**Built by Programmify with ❤️**
