# 📚 Alpaca Trading Course - Lesson 29

## 🚀 Your Bot Online 24/7 – Deploying to a VPS Server

### 🎯 What You Will Learn

In this lesson, you will learn how to **deploy your trading bot to a Virtual Private Server (VPS)**, ensuring it runs 24/7, 365 days a year without requiring your laptop to be on or connected to the internet.

You'll discover:

- ✅ Why running a bot on your laptop is insufficient for serious trading
- ✅ What a VPS is and why it's essential for algorithmic trading
- ✅ Step-by-step VPS setup and configuration
- ✅ Deploying your bot code to a remote server
- ✅ Using systemd to keep your bot running as a service
- ✅ Monitoring and managing your deployed bot

By the end of this lesson, your bot will be a fully autonomous agent running in a secure, professional cloud environment.

---

## 📖 Why This Matters

### The Problem: Running a Bot on Your Laptop

When you run your trading bot on your local machine, you face several critical limitations:

1. **Reliability Issues:**
   - Your home internet connection is not 100% reliable
   - Your laptop needs to be rebooted for updates
   - Power outages will stop your bot
   - Network interruptions can cause missed trades

2. **Uptime Requirements:**
   - Trading bots need to run continuously during market hours (or 24/7 for crypto)
   - You can't monitor it personally 24/7
   - Any downtime means missed opportunities

3. **Resource Constraints:**
   - Your laptop is for work and entertainment
   - Running a bot uses CPU and memory
   - Background processes can interfere with your work

### The Solution: Virtual Private Server (VPS)

A VPS is a small slice of a powerful server that you rent from a cloud provider. Think of it as your own personal computer located in a highly secure and reliable data center.

**Benefits:**
- ✅ **Dedicated IP address** - Always accessible
- ✅ **Guaranteed uptime** - Usually >99.9%
- ✅ **Stable, high-speed internet** - No home network issues
- ✅ **Your choice of OS** - We'll use Linux (Ubuntu)
- ✅ **Affordable** - Just a few dollars per month
- ✅ **Professional** - This is how real trading systems run

---

## 🚀 Quick Start

### Prerequisites

Before deploying, ensure you have:

1. ✅ A working trading bot (from previous lessons)
2. ✅ Your bot code in a Git repository (GitHub recommended)
3. ✅ A `requirements.txt` file with all dependencies
4. ✅ A `config.json` or `config.py` template (never commit real keys!)

### Step 1: Choose a VPS Provider

Recommended providers (all offer excellent value):

- **Hetzner** - Often praised for best value
- **DigitalOcean** - User-friendly, great documentation
- **Linode** - Reliable, good support
- **Vultr** - Fast, global locations

**Recommended Specs:**
- **CPU:** 1 vCPU (more than enough for a single bot)
- **RAM:** 1-2 GB
- **Storage:** 20-40 GB SSD
- **OS:** Ubuntu 22.04 LTS
- **Cost:** $3-6/month

### Step 2: Create Your VPS

1. **Sign Up:** Create an account with your chosen provider
2. **Create Server:**
   - **Location:** Choose close to you or the exchange's servers (USA recommended)
   - **OS:** Ubuntu 22.04 LTS
   - **Plan:** Cheapest plan (1 vCPU, 1-2 GB RAM)
   - **Authentication:** ⚠️ **CRITICAL** - Choose SSH Key (not password!)
3. **Launch:** Click "Create" or "Deploy"
4. **Note Your IP:** Save the public IP address you receive

### Step 3: Generate SSH Key (If Needed)

If you don't have an SSH key pair:

**Windows (PowerShell):**
```powershell
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter to accept default location
# Press Enter twice for no passphrase (or set one)
```

**macOS/Linux:**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

**Upload Public Key:**
- Copy the contents of `~/.ssh/id_ed25519.pub` (or `id_rsa.pub`)
- Paste it into your VPS provider's SSH key section

### Step 4: Connect to Your VPS

**Windows (PowerShell):**
```powershell
ssh root@YOUR_SERVER_IP_ADDRESS
```

**macOS/Linux:**
```bash
ssh root@YOUR_SERVER_IP_ADDRESS
```

Replace `YOUR_SERVER_IP_ADDRESS` with the IP address from Step 2.

---

## 📋 Deployment Guide

### Step 1: Update System

Always update your server first:

```bash
apt update && apt upgrade -y
```

### Step 2: Install Required Software

```bash
# Install Python, pip, and venv
apt install python3-pip python3-venv git -y
```

### Step 3: Clone Your Repository

```bash
# Navigate to home directory
cd ~

# Clone your repository (replace with your actual repo URL)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Navigate into your project folder
cd YOUR_REPO_NAME
```

**Note:** If your bot is in a subfolder (e.g., `Alpaca25/`), navigate there:
```bash
cd Alpaca25
```

### Step 4: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 5: Create Configuration File

**⚠️ IMPORTANT:** Never commit your real `config.json` or `config.py` to Git!

```bash
# Copy the example config
cp config.example.json config.json

# Edit with nano (or your preferred editor)
nano config.json
```

Paste your actual API keys and configuration. Save and exit:
- **Nano:** `Ctrl+X`, then `Y`, then `Enter`
- **Vi/Vim:** `:wq` (write and quit)

### Step 6: Test Your Bot

Before setting up as a service, test that it runs:

```bash
# Make sure you're in the project directory with venv activated
source venv/bin/activate

# Run your bot (replace with your actual script name)
python resilient_bot.py
```

If it works, press `Ctrl+C` to stop it.

---

## 🔧 Setting Up systemd Service

systemd is the modern way to manage services on Linux. It will:
- ✅ Start your bot automatically on server boot
- ✅ Restart your bot if it crashes
- ✅ Keep it running in the background
- ✅ Provide easy status and log viewing

### Step 1: Create Service File

```bash
nano /etc/systemd/system/trading-bot.service
```

### Step 2: Paste Service Configuration

Copy the template below, **replacing the paths** with your actual project path:

```ini
[Unit]
Description=Alpaca Trading Bot
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/root/YOUR_PROJECT_FOLDER
Environment="PATH=/root/YOUR_PROJECT_FOLDER/venv/bin"
ExecStart=/root/YOUR_PROJECT_FOLDER/venv/bin/python /root/YOUR_PROJECT_FOLDER/YOUR_BOT_SCRIPT.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Replace:**
- `/root/YOUR_PROJECT_FOLDER` - Your actual project path (e.g., `/root/AlpacaTutorial/Alpaca25`)
- `YOUR_BOT_SCRIPT.py` - Your bot's Python file (e.g., `resilient_bot.py`)

**Example:**
```ini
[Unit]
Description=Alpaca Trading Bot
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/root/AlpacaTutorial/Alpaca25
Environment="PATH=/root/AlpacaTutorial/Alpaca25/venv/bin"
ExecStart=/root/AlpacaTutorial/Alpaca25/venv/bin/python /root/AlpacaTutorial/Alpaca25/resilient_bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Save and exit (`Ctrl+X`, `Y`, `Enter`).

### Step 3: Enable and Start Service

```bash
# Reload systemd to recognize the new service
systemctl daemon-reload

# Start the service
systemctl start trading-bot

# Enable it to start on boot
systemctl enable trading-bot

# Check status
systemctl status trading-bot
```

### Step 4: View Logs

```bash
# View recent logs
journalctl -u trading-bot -n 50

# Follow logs in real-time (like tail -f)
journalctl -u trading-bot -f

# View logs from today
journalctl -u trading-bot --since today
```

---

## 📊 Managing Your Bot

### Check Status

```bash
systemctl status trading-bot
```

### Stop Bot

```bash
systemctl stop trading-bot
```

### Start Bot

```bash
systemctl start trading-bot
```

### Restart Bot

```bash
systemctl restart trading-bot
```

### Disable Auto-Start on Boot

```bash
systemctl disable trading-bot
```

### View Logs

```bash
# Last 100 lines
journalctl -u trading-bot -n 100

# Follow in real-time
journalctl -u trading-bot -f

# Since specific date
journalctl -u trading-bot --since "2024-01-15"

# Between dates
journalctl -u trading-bot --since "2024-01-15" --until "2024-01-16"
```

---

## 🔄 Updating Your Bot

When you make changes to your bot code:

### Method 1: Git Pull (Recommended)

```bash
# Navigate to your project
cd ~/YOUR_PROJECT_FOLDER

# Pull latest changes
git pull

# Restart the service
systemctl restart trading-bot

# Check status
systemctl status trading-bot
```

### Method 2: Manual Upload

```bash
# Stop the bot
systemctl stop trading-bot

# Upload new files (use SCP, SFTP, or edit directly)
# Then restart
systemctl start trading-bot
```

---

## 🐛 Troubleshooting

### Problem: "Service failed to start"

**Check logs:**
```bash
journalctl -u trading-bot -n 50
```

**Common causes:**
1. **Wrong path in service file** - Verify `WorkingDirectory` and `ExecStart` paths
2. **Missing dependencies** - Run `pip install -r requirements.txt` again
3. **Config file missing** - Ensure `config.json` exists in project folder
4. **Python path wrong** - Verify venv path in `ExecStart`

### Problem: "Bot starts but immediately stops"

**Check logs:**
```bash
journalctl -u trading-bot -n 100
```

**Common causes:**
1. **API keys invalid** - Check `config.json`
2. **Import errors** - Check if all dependencies are installed
3. **File not found** - Check if all required files exist
4. **Permission issues** - Ensure files are readable

### Problem: "Can't connect to server via SSH"

**Solutions:**
1. Check if server is running (provider dashboard)
2. Verify IP address is correct
3. Check firewall settings (port 22 should be open)
4. Verify SSH key is correct

### Problem: "Bot not responding to market changes"

**Check:**
1. View logs: `journalctl -u trading-bot -f`
2. Verify API keys are correct
3. Check if market is open
4. Verify network connectivity: `ping 8.8.8.8`

### Problem: "Service won't restart after crash"

**Check restart policy:**
```bash
# View service file
cat /etc/systemd/system/trading-bot.service

# Ensure Restart=always is set
# Then reload and restart
systemctl daemon-reload
systemctl restart trading-bot
```

---

## 🔐 Security Best Practices

### ✅ What This Guide Does Right

1. **SSH Key Authentication** - More secure than passwords
2. **Separate Config File** - API keys not in Git
3. **Virtual Environment** - Isolated dependencies
4. **Service Isolation** - Bot runs as dedicated service

### ⚠️ Additional Recommendations

1. **Firewall Setup:**
   ```bash
   # Install UFW (Uncomplicated Firewall)
   apt install ufw -y
   
   # Allow SSH
   ufw allow 22/tcp
   
   # Enable firewall
   ufw enable
   ```

2. **Regular Updates:**
   ```bash
   # Update system weekly
   apt update && apt upgrade -y
   ```

3. **Backup Configuration:**
   - Keep a secure backup of your `config.json`
   - Never share your API keys
   - Rotate keys regularly

4. **Monitor Logs:**
   - Check logs regularly for errors
   - Set up alerts for critical failures
   - Monitor bot performance

5. **Use Non-Root User (Advanced):**
   - Create a dedicated user for the bot
   - Run service as that user instead of root
   - Improves security isolation

---

## 📁 Project Structure

After deployment, your VPS will have:

```
/root/YOUR_PROJECT_FOLDER/
├── resilient_bot.py          # Your bot script
├── config.json               # Your API keys (not in Git!)
├── config.example.json       # Template (in Git)
├── requirements.txt          # Dependencies
├── state.json                # Bot state (if applicable)
├── trading_bot.log           # Log file (if applicable)
├── venv/                     # Virtual environment
└── .git/                     # Git repository
```

---

## 🎓 Key Takeaways

1. **VPS is Essential** - Professional trading requires 24/7 uptime
2. **systemd is Powerful** - Keeps your bot running automatically
3. **Git Simplifies Updates** - Easy to deploy code changes
4. **Logs are Critical** - Always check logs when troubleshooting
5. **Security Matters** - Use SSH keys, protect API keys
6. **Test Before Deploy** - Always test locally first
7. **Monitor Regularly** - Check bot status and logs frequently

---

## 📚 Additional Resources

### VPS Providers
- [Hetzner](https://www.hetzner.com/)
- [DigitalOcean](https://www.digitalocean.com/)
- [Linode](https://www.linode.com/)
- [Vultr](https://www.vultr.com/)

### Linux & systemd
- [systemd Service Tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units)
- [Ubuntu Server Guide](https://ubuntu.com/server/docs)
- [SSH Key Setup Guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-2)

### Git & Deployment
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Documentation](https://docs.github.com/)

---

## 📝 License

This is educational material for learning algorithmic trading with Alpaca API.

---

## ⚠️ Disclaimer

This guide is for educational purposes only. Trading involves substantial risk of loss. Always:

- ✅ Test strategies thoroughly with paper trading
- ✅ Never risk more than you can afford to lose
- ✅ Understand the strategy before deploying
- ✅ Monitor your strategies regularly
- ✅ Use proper security practices
- ✅ Keep backups of your configuration

**Past performance does not guarantee future results.**

---

## 💬 Support

Found an issue? Have questions?

- Check the troubleshooting section above
- Review the service logs: `journalctl -u trading-bot -n 100`
- Verify your configuration files
- Check Alpaca API status: https://status.alpaca.markets/

---

**"Risk comes from not knowing what you're doing." - Warren Buffett**

Congratulations! You've achieved a milestone that separates hobbyists from serious algorithmic traders. Your bot is no longer a script on your laptop; it is a fully autonomous agent, running 24/7 in a secure, professional environment. You can now close your laptop, go on vacation, and trust that your bot is diligently watching the markets for you! 🚀

---

*Alpaca Trading Course - Lesson 29*  
*Your Bot Online 24/7 – Deploying to a VPS Server*

