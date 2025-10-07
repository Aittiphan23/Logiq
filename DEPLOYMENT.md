# 🚀 Logiq Deployment Guide

Complete guide for deploying Logiq to various platforms.

---

## 📋 Prerequisites

Before deploying, ensure you have:

- ✅ Discord Bot Token
- ✅ MongoDB instance (or MongoDB Atlas account)
- ✅ OpenAI API Key (for AI features)
- ✅ All configuration values ready

---

## 🐳 Docker Deployment (Recommended)

### Local Docker

1. **Setup environment**
```bash
cp .env.example .env
nano .env  # Edit with your values
```

2. **Build and run**
```bash
docker-compose up -d
```

3. **Check logs**
```bash
docker-compose logs -f bot
```

4. **Stop**
```bash
docker-compose down
```

### Docker Production

1. **Build optimized image**
```bash
docker build -t Logiq:latest .
```

2. **Run with production settings**
```bash
docker run -d \
  --name Logiq \
  -e DISCORD_BOT_TOKEN=your_token \
  -e MONGODB_URI=your_mongo_uri \
  -e OPENAI_API_KEY=your_key \
  -p 8000:8000 \
  --restart unless-stopped \
  Logiq:latest
```

---

## ☁️ Cloud Platforms

### Railway (Easiest)

1. **Create Railway account**: https://railway.app
2. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

3. **Initialize project**
```bash
railway init
```

4. **Add MongoDB**
```bash
railway add mongodb
```

5. **Set environment variables**
```bash
railway variables set DISCORD_BOT_TOKEN=your_token
railway variables set OPENAI_API_KEY=your_key
```

6. **Deploy**
```bash
railway up
```

7. **View logs**
```bash
railway logs
```

### Heroku

1. **Install Heroku CLI**
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login and create app**
```bash
heroku login
heroku create Logiq
```

3. **Add MongoDB**
```bash
heroku addons:create mongolab:sandbox
```

4. **Set environment variables**
```bash
heroku config:set DISCORD_BOT_TOKEN=your_token
heroku config:set OPENAI_API_KEY=your_key
```

5. **Create Procfile**
```
worker: python main.py
```

6. **Deploy**
```bash
git push heroku main
```

7. **Scale worker**
```bash
heroku ps:scale worker=1
```

8. **View logs**
```bash
heroku logs --tail
```

### AWS EC2

1. **Launch EC2 instance**
   - Ubuntu 22.04 LTS
   - t2.small or larger
   - Open port 8000 for API (optional)

2. **Connect via SSH**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install dependencies**
```bash
sudo apt update
sudo apt install -y python3.11 python3-pip git
```

4. **Clone repository**
```bash
git clone https://github.com/yourusername/Logiq.git
cd Logiq
```

5. **Setup virtual environment**
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Configure environment**
```bash
cp .env.example .env
nano .env  # Add your values
```

7. **Run with systemd**

Create `/etc/systemd/system/Logiq.service`:
```ini
[Unit]
Description=Logiq Discord Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Logiq
Environment="PATH=/home/ubuntu/Logiq/venv/bin"
ExecStart=/home/ubuntu/Logiq/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

8. **Start service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable Logiq
sudo systemctl start Logiq
sudo systemctl status Logiq
```

9. **View logs**
```bash
sudo journalctl -u Logiq -f
```

### AWS ECS (Fargate)

1. **Build and push Docker image**
```bash
# Authenticate to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Create repository
aws ecr create-repository --repository-name Logiq

# Build and tag
docker build -t Logiq .
docker tag Logiq:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/Logiq:latest

# Push
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/Logiq:latest
```

2. **Create ECS cluster**
```bash
aws ecs create-cluster --cluster-name Logiq-cluster
```

3. **Create task definition** (`task-definition.json`)
```json
{
  "family": "Logiq",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "Logiq",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/Logiq:latest",
      "environment": [
        {"name": "DISCORD_BOT_TOKEN", "value": "your_token"},
        {"name": "MONGODB_URI", "value": "your_mongo_uri"},
        {"name": "OPENAI_API_KEY", "value": "your_key"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/Logiq",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

4. **Register task**
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

5. **Create service**
```bash
aws ecs create-service \
  --cluster Logiq-cluster \
  --service-name Logiq-service \
  --task-definition Logiq \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Digital Ocean

1. **Create Droplet**
   - Ubuntu 22.04
   - Basic plan ($6/month)
   - Enable monitoring

2. **SSH into droplet**
```bash
ssh root@your-droplet-ip
```

3. **Install Docker**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

4. **Install Docker Compose**
```bash
apt install docker-compose -y
```

5. **Clone and configure**
```bash
git clone https://github.com/yourusername/Logiq.git
cd Logiq
cp .env.example .env
nano .env
```

6. **Start with Docker Compose**
```bash
docker-compose up -d
```

7. **Setup auto-start**
```bash
# Docker Compose starts automatically with Docker
systemctl enable docker
```

---

## 🗄️ Database Setup

### MongoDB Atlas (Recommended for Production)

1. **Create account**: https://www.mongodb.com/cloud/atlas
2. **Create cluster** (Free tier available)
3. **Create database user**
4. **Whitelist IP**: Add 0.0.0.0/0 for all IPs (or specific IPs)
5. **Get connection string**
6. **Update .env**:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/Logiq
```

### Self-hosted MongoDB

```bash
# Install MongoDB
sudo apt install -y mongodb

# Start service
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Create database and user
mongosh
use Logiq
db.createUser({
  user: "botuser",
  pwd: "secure_password",
  roles: ["readWrite"]
})
```

---

## 🔐 Environment Variables

Required:
```env
DISCORD_BOT_TOKEN=your_discord_bot_token
MONGODB_URI=mongodb://localhost:27017  # or MongoDB Atlas URI
```

Optional:
```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
YOUTUBE_API_KEY=your_youtube_key
SPOTIFY_CLIENT_ID=your_spotify_id
SPOTIFY_CLIENT_SECRET=your_spotify_secret
ENVIRONMENT=production
```

---

## 📊 Monitoring

### Health Checks

```bash
# Check if bot is running
curl http://your-domain:8000/health

# Check stats
curl http://your-domain:8000/stats
```

### Logs

```bash
# Docker
docker-compose logs -f bot

# Systemd
sudo journalctl -u Logiq -f

# File logs
tail -f logs/bot.log
```

### Uptime Monitoring

Use services like:
- UptimeRobot
- Pingdom
- StatusCake

---

## 🔄 Updates

### Docker
```bash
git pull
docker-compose down
docker-compose up -d --build
```

### Systemd
```bash
cd /path/to/Logiq
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart Logiq
```

---

## 🆘 Troubleshooting

### Bot won't start
1. Check environment variables
2. Verify MongoDB connection
3. Check Discord token
4. Review logs

### Database connection failed
1. Verify MongoDB is running
2. Check connection string
3. Verify network access
4. Check credentials

### Commands not appearing
1. Run `/sync` command
2. Wait 1 hour for global sync
3. Check bot permissions
4. Verify intents are enabled

---

## 🔒 Security Best Practices

1. **Never commit secrets**
2. **Use environment variables**
3. **Enable 2FA on all accounts**
4. **Regular updates**
5. **Monitor logs**
6. **Use firewall rules**
7. **Restrict database access**
8. **Regular backups**

---

## 📈 Scaling

### Horizontal Scaling
- Use load balancer
- Multiple bot instances
- Shared database
- Redis for caching

### Vertical Scaling
- Increase CPU/RAM
- Optimize queries
- Cache frequently accessed data
- Use connection pooling

---

## 💾 Backup

### Automated Backup Script

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/Logiq"

# MongoDB backup
mongodump --uri="$MONGODB_URI" --out="$BACKUP_DIR/mongo_$DATE"

# Compress
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" "$BACKUP_DIR/mongo_$DATE"

# Remove old backups (keep last 7 days)
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete
```

### Restore

```bash
mongorestore --uri="$MONGODB_URI" /path/to/backup
```

---

## 📞 Support

For deployment issues:
- Check logs first
- Review this guide
- Open GitHub issue
- Join support Discord

---

**Happy Deploying! 🚀**
