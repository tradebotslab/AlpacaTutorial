# Lesson 29: **Your Bot Online 24/7 – Deploying to a VPS Server**

Welcome to Lesson 29 of the Alpaca Trading Course! This lesson teaches you how to deploy your trading bot to a Virtual Private Server (VPS), ensuring it runs 24/7, 365 days a year without requiring your laptop to be on or connected to the internet.

## The Problem: Running a Bot on Your Laptop

When you run your trading bot on your local machine, you face several critical limitations: reliability issues (home internet not 100% reliable, laptop needs reboots for updates, power outages stop your bot, network interruptions cause missed trades), uptime requirements (trading bots need to run continuously during market hours, you can't monitor personally 24/7, any downtime means missed opportunities), and resource constraints (laptop is for work/entertainment, running a bot uses CPU/memory, background processes interfere with work).

| Problem/Challenge | Description |
|---|---|
| **Unreliable Connection** | Home internet is not 100% reliable |
| **Uptime Issues** | Laptop reboots, power outages, network interruptions stop your bot |
| **Resource Constraints** | Running bot uses CPU/memory, interferes with other work |
| **No 24/7 Operation** | Cannot run continuously without keeping laptop on |

## The Solution: Deploy to a Virtual Private Server (VPS)

The solution is to deploy your bot to a VPS - a small slice of a powerful server you rent from a cloud provider. A VPS provides: dedicated IP address (always accessible), guaranteed uptime (usually >99.9%), stable high-speed internet (no home network issues), your choice of OS (we'll use Linux Ubuntu), affordable cost (just a few dollars per month), and professional operation (this is how real trading systems run).

### Step 29.1: Choose a VPS Provider

Recommended providers: Hetzner, DigitalOcean, Linode, Vultr. Recommended specs: 1 vCPU, 1-2 GB RAM, 20-40 GB SSD, Ubuntu 22.04 LTS, cost $3-6/month.

### Step 29.2: Create Your VPS

1. Sign up with your chosen provider
2. Create server: Choose location (USA recommended), OS (Ubuntu 22.04 LTS), Plan (cheapest plan), Authentication (choose SSH Key, not password!)
3. Launch and note your public IP address

### Step 29.3: Deploy Your Bot

1. Connect via SSH: `ssh root@YOUR_SERVER_IP_ADDRESS`
2. Update system: `apt update && apt upgrade -y`
3. Install required software: `apt install python3-pip python3-venv git -y`
4. Clone your repository: `git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git`
5. Set up Python environment: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
6. Create config file: `cp config.example.json config.json` and edit with your API keys

### Step 29.4: Set Up systemd Service

Create a service file `/etc/systemd/system/trading-bot.service` to keep your bot running as a service that starts on boot and restarts if it crashes.

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **SSH Key Authentication** | More secure than passwords - always use SSH keys |
| **systemd Services** | Use systemd to keep bot running 24/7 and restart on crashes |
| **Git for Updates** | Use Git to easily deploy code changes |
| **Monitor Logs** | Use `journalctl -u trading-bot -f` to monitor bot activity |
| **Security** | Set up firewall (UFW), keep system updated, protect API keys |

## Conclusion

You've successfully learned how to deploy your trading bot to a VPS server! Your bot is now running 24/7 in a secure, professional cloud environment. You can close your laptop, go on vacation, and trust that your bot is diligently watching the markets. This is a milestone that separates hobbyists from serious algorithmic traders. In the final lesson, you'll learn about statistical arbitrage and pairs trading - advanced market-neutral strategies.
