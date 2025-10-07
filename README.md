# 🤖 Logiq

**AI-Enhanced Discord Bot for Community Management, Productivity, and Entertainment**

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.4.0-blue)](https://github.com/Rapptz/discord.py)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🌟 Features

### 🔐 Verification System
- Button-based verification
- CAPTCHA verification
- Custom welcome messages
- Automatic role assignment

### 🛡️ Moderation
- **Commands**: `/warn`, `/mute`, `/kick`, `/ban`, `/unban`, `/timeout`
- AI-powered auto-moderation
- Spam detection
- Toxicity filtering
- Comprehensive logging

### 🎭 Roles
- Self-assignable role menus
- Reaction roles
- Role information commands
- Temporary roles

### 📈 Leveling System
- XP from messages and voice activity
- Custom rank cards
- Leaderboards
- Level-up notifications

### 💎 Economy
- Virtual currency (ProgrammiCoins)
- Daily rewards
- Shop system
- Gambling games (coinflip, roulette)
- User-to-user transactions

### 🤖 AI Integration
- AI chatbot (OpenAI/Anthropic)
- Conversation summarization
- Content moderation
- Smart auto-responses

### 🎵 Music (Placeholder)
- YouTube/Spotify playback
- Queue management
- Audio controls

### 🎫 Tickets
- Support ticket system
- Private ticket channels
- Category-based organization

### 📊 Analytics
- Server statistics
- Activity tracking
- Growth metrics
- User engagement analytics

### 🎮 Games
- Trivia
- Roulette
- Coinflip
- Dice rolling
- Magic 8-ball

### ⚙️ Utility
- Polls
- Reminders
- Server/User info
- Avatar display

### 🔧 Admin
- Module management
- Command syncing
- Cog reloading
- Configuration viewing

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- MongoDB 7.0+
- Discord Bot Token
- OpenAI API Key (optional, for AI features)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Logiq.git
cd Logiq
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your tokens and configuration
```

5. **Update config.yaml**
```yaml
# Edit config.yaml with your server-specific settings
```

6. **Run the bot**
```bash
python main.py
```

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

2. **Start all services**
```bash
docker-compose up -d
```

3. **View logs**
```bash
docker-compose logs -f bot
```

4. **Stop services**
```bash
docker-compose down
```

### Services Included
- **bot**: Discord bot
- **mongodb**: MongoDB database
- **redis**: Redis cache (optional)

---

## 📋 Configuration

### Environment Variables (.env)

```env
# Discord
DISCORD_BOT_TOKEN=your_bot_token_here

# Database
MONGODB_URI=mongodb://localhost:27017

# AI Services
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Music (Optional)
YOUTUBE_API_KEY=your_youtube_key_here
SPOTIFY_CLIENT_ID=your_spotify_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_secret_here

# Environment
ENVIRONMENT=production
```

### Configuration File (config.yaml)

See `config.yaml` for detailed configuration options including:
- Module enable/disable
- XP rates and rewards
- Currency settings
- AI parameters
- Auto-moderation rules

---

## 📚 Commands Reference

### Verification
- `/setup-verification` - Configure verification system
- `/send-verification` - Send verification message

### Moderation
- `/warn <user> <reason>` - Warn a user
- `/warnings <user>` - View user warnings
- `/timeout <user> <duration> <reason>` - Timeout user
- `/kick <user> <reason>` - Kick user
- `/ban <user> <reason>` - Ban user
- `/unban <user_id>` - Unban user

### Roles
- `/role-menu <roles>` - Create role selection menu
- `/addrole <user> <role>` - Add role to user
- `/removerole <user> <role>` - Remove role from user
- `/roleinfo <role>` - Get role information

### Leveling
- `/rank [user]` - View rank card
- `/leaderboard` - View XP leaderboard
- `/setlevel <user> <level>` - Set user level (Admin)

### Economy
- `/balance [user]` - Check balance
- `/daily` - Claim daily reward
- `/give <user> <amount>` - Give currency
- `/coinflip <amount> <choice>` - Flip coin
- `/shop` - View shop

### AI
- `/ask <question>` - Ask AI a question
- `/summarize [count]` - Summarize messages
- `/clear-conversation` - Clear AI history

### Utility
- `/poll <question> <options>` - Create poll
- `/remind <duration> <message>` - Set reminder
- `/serverstats` - Server statistics
- `/userinfo [user]` - User information
- `/avatar [user]` - Get user avatar

### Tickets
- `/ticket-setup <category> [role]` - Setup tickets
- `/ticket-panel` - Send ticket panel
- `/close-ticket [reason]` - Close ticket

### Analytics
- `/analytics [days]` - View analytics
- `/activity` - View recent activity

### Games
- `/trivia` - Play trivia
- `/roulette <bet> <choice>` - Play roulette
- `/dice [sides]` - Roll dice
- `/8ball <question>` - Magic 8-ball

### Admin
- `/reload <cog>` - Reload cog
- `/sync` - Sync commands
- `/modules` - View modules
- `/botinfo` - Bot information
- `/config` - View configuration
- `/purge <amount>` - Delete messages

---

## 🏗️ Architecture

```
Logiq/
├── main.py                 # Entry point
├── config.yaml            # Configuration
├── requirements.txt       # Dependencies
│
├── cogs/                  # Command modules
│   ├── verification.py
│   ├── moderation.py
│   ├── roles.py
│   ├── leveling.py
│   ├── economy.py
│   ├── ai_chat.py
│   ├── utility.py
│   ├── music.py
│   ├── tickets.py
│   ├── analytics.py
│   ├── games.py
│   └── admin.py
│
├── database/              # Database layer
│   ├── db_manager.py
│   └── models.py
│
├── utils/                 # Utilities
│   ├── embeds.py
│   ├── logger.py
│   ├── permissions.py
│   ├── converters.py
│   └── constants.py
│
├── web/                   # Web API
│   └── api.py
│
└── tests/                 # Unit tests
    ├── test_database.py
    └── test_utils.py
```

---

## 🌐 Web API

When web module is enabled, the bot exposes a REST API on port 8000.

### Endpoints

- `GET /` - API information
- `GET /stats` - Bot statistics
- `GET /guilds` - List guilds
- `GET /guilds/{guild_id}` - Guild details
- `GET /guilds/{guild_id}/leaderboard` - Guild leaderboard
- `GET /guilds/{guild_id}/analytics` - Guild analytics
- `GET /health` - Health check
- `GET /modules` - Module status

### Example
```bash
curl http://localhost:8000/stats
```

---

## 🧪 Testing

Run unit tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

---

## 📊 Database Schema

### Collections

- **users**: User data (XP, balance, inventory, warnings)
- **guilds**: Guild configuration
- **tickets**: Support tickets
- **analytics**: Event logs
- **reminders**: Scheduled reminders
- **shop**: Shop items

---

## 🔒 Security

- Never commit `.env` file
- Use environment variables for sensitive data
- Implement rate limiting
- Validate all user inputs
- Use Discord permissions properly
- Regular security audits

---

## 🚢 Deployment

### Railway

1. Create new project
2. Add MongoDB plugin
3. Add environment variables
4. Deploy from GitHub
5. Configure domain (optional)

### AWS ECS

1. Build Docker image
2. Push to ECR
3. Create ECS cluster
4. Create task definition
5. Deploy service
6. Configure load balancer

### Heroku

1. Create app
2. Add MongoDB addon
3. Set environment variables
4. Deploy via Git
5. Scale dynos

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper
- [Motor](https://github.com/mongodb/motor) - Async MongoDB driver
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [OpenAI](https://openai.com/) - AI services

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/Logiq/issues)
- **Discord**: [Support Server](https://discord.gg/your-invite)
- **Documentation**: [Wiki](https://github.com/yourusername/Logiq/wiki)

---

## 🗺️ Roadmap

- [ ] Advanced music features
- [ ] Web dashboard UI
- [ ] Custom commands system
- [ ] Backup/restore functionality
- [ ] Multi-language support
- [ ] Advanced analytics charts
- [ ] Integration with more AI providers
- [ ] Premium features

---

**Made with ❤️ by the Logiq team**
