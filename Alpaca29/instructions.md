Lesson 29: Your Bot Online 24/7 – Deploying to a VPS Server
Welcome to Lesson 29. You have a smart, resilient, data-streaming bot. There's just one problem: it only runs when your laptop is on and connected to the internet. If you close your laptop lid, lose Wi-Fi, or have a power outage, your bot goes offline. This is unacceptable for any serious trading operation.

In this lesson, you will learn how to deploy your trading bot to a Virtual Private Server (VPS), a small, cheap, and reliable computer in the cloud that will run your code 24/7, 365 days a year.

Why You Can't Run a Bot on Your Laptop
Reliability: Your home internet connection is not 100% reliable. Your laptop needs to be rebooted. Power can go out.

Uptime: You want your bot to run continuously during market hours (or 24/7 for crypto) without you needing to monitor it personally.

Resources: Your laptop is for your work and entertainment. Running a trading bot, even a lightweight one, uses CPU and memory that you need for other tasks.

What is a VPS?
A Virtual Private Server is a small slice of a powerful server that you rent from a cloud provider. Think of it as your own personal computer located in a highly secure and reliable data center. It comes with:

A dedicated IP address.

Guaranteed uptime (usually >99.9%).

A stable, high-speed internet connection.

Your choice of operating system (we'll use Linux).

For a simple Python bot, you can get a powerful enough VPS for just a few dollars a month from providers like Hetzner, DigitalOcean, Linode, or Vultr.

The Deployment Process: A Step-by-Step Guide
This guide will walk you through the general steps. Specific clicks may vary slightly between providers, but the principles are universal.

Step 1: Create and Configure Your VPS
Sign Up: Choose a provider (Hetzner is often praised for its value) and create an account.

Create a Server/Droplet/Instance:

Location: Pick a location physically close to you or the exchange's servers (e.g., in the USA).

Operating System: Choose Ubuntu 22.04 LTS. It's the most common and well-supported Linux distribution.

Plan: Select the cheapest plan available. It will be more than enough for a single bot (e.g., 1 vCPU, 1-2 GB RAM).

Authentication: This is critical. Choose SSH Key. Follow the provider's guide to generate an SSH key pair on your local machine and upload the public key. This is far more secure than using a password.

Launch: Click "Create" or "Deploy". Within a minute, your server will be online, and you'll be given its public IP address.

Step 2: Connect to and Prepare the Server
You'll use the command line to connect to your new server via SSH (Secure Shell).

Connect: Open your terminal (or PowerShell on Windows) and connect as the root user.

bash
ssh root@YOUR_SERVER_IP_ADDRESS
Update the System: The first thing you should always do on a new server is update its software packages.

bash
apt update && apt upgrade -y
Install Python: Install Python, the pip package manager, and the venv module for virtual environments.

bash
apt install python3-pip python3-venv -y
Step 3: Deploy Your Bot's Code
Use Git (Recommended): The best way to get your code onto the server is by cloning it from a Git repository (like GitHub).

First, install Git: apt install git -y

Then, clone your project: git clone your_repository_url.git
This makes updating your bot as simple as running git pull on the server.

Create requirements.txt: On your local machine, generate a list of your project's dependencies:

bash
# In your project folder on your laptop
pip freeze > requirements.txt
Commit and push this file to your Git repository so it's available on the server.

Set Up the Environment:

Navigate into your project folder on the server: cd your_project_folder

Create a virtual environment: python3 -m venv venv

Activate it: source venv/bin/activate

Install dependencies: pip install -r requirements.txt

Create Your Config File:
Your config.json should never be in your Git repository. You must create it directly on the server.

Use a simple text editor like nano: nano config.json

Paste in your configuration (API keys, webhook URL, etc.).

Save and exit (Ctrl+X, then Y, then Enter).

Step 4: Keep the Bot Running with systemd
If you run python your_bot.py and then close your SSH session, the bot will stop. We need to tell the server's operating system to manage our script as a persistent service. The modern way to do this on Linux is with systemd.

Create a Service File:

bash
nano /etc/systemd/system/trading-bot.service
Paste the Service Configuration:
Copy the template below, making sure to replace /root/your_project_folder with the actual path to your project and your_bot.py with your main script's filename.

ini
[Unit]
Description=Alpaca Trading Bot
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/your_project_folder
ExecStart=/root/your_project_folder/venv/bin/python your_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
Manage the Service:

Reload systemd to make it aware of your new service file:

bash
systemctl daemon-reload
Start your bot:

bash
systemctl start trading-bot
Check its status and logs: This is how you see your print statements and errors!

bash
systemctl status trading-bot
# Press 'q' to exit the status view
Enable it to start on boot: This is the magic command that makes your bot restart automatically if the server itself reboots.

bash
systemctl enable trading-bot
Conclusion
Congratulations! You have achieved a milestone that separates hobbyists from serious algorithmic traders. Your bot is no longer a script on your laptop; it is a fully autonomous agent, running 24/7 in a secure, professional environment. You can now close your laptop, go on vacation, and trust that your bot is diligently watching the markets for you, sending you Discord notifications along the way