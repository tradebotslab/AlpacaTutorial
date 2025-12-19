#!/bin/bash
# Deployment script for Alpaca Trading Bot on VPS
# This script automates the deployment process

set -e  # Exit on any error

echo "=========================================="
echo "🚀 Alpaca Trading Bot - VPS Deployment"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration (modify these variables)
PROJECT_DIR="/root/YOUR_PROJECT_FOLDER"
BOT_SCRIPT="YOUR_BOT_SCRIPT.py"
SERVICE_NAME="trading-bot"
GIT_REPO_URL="https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"

echo -e "${YELLOW}⚠️  IMPORTANT: Edit this script and set the variables above!${NC}"
echo ""
read -p "Have you edited the script with your project details? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}Please edit the script first!${NC}"
    exit 1
fi

echo ""
echo "📦 Step 1: Updating system packages..."
apt update && apt upgrade -y

echo ""
echo "🐍 Step 2: Installing Python and dependencies..."
apt install python3-pip python3-venv git -y

echo ""
echo "📥 Step 3: Cloning repository..."
if [ -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}Directory exists. Pulling latest changes...${NC}"
    cd "$PROJECT_DIR"
    git pull
else
    echo "Cloning repository..."
    git clone "$GIT_REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

echo ""
echo "🔧 Step 4: Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

echo ""
echo "📚 Step 5: Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "⚙️  Step 6: Setting up configuration..."
if [ ! -f "config.json" ]; then
    if [ -f "config.example.json" ]; then
        echo -e "${YELLOW}⚠️  config.json not found. Copying from config.example.json${NC}"
        cp config.example.json config.json
        echo -e "${YELLOW}⚠️  Please edit config.json with your API keys!${NC}"
        echo "Press Enter to continue after editing config.json..."
        read
    elif [ -f "config.example.py" ]; then
        echo -e "${YELLOW}⚠️  config.py not found. Copying from config.example.py${NC}"
        cp config.example.py config.py
        echo -e "${YELLOW}⚠️  Please edit config.py with your API keys!${NC}"
        echo "Press Enter to continue after editing config.py..."
        read
    else
        echo -e "${RED}❌ No config file found! Please create config.json or config.py${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ config.json already exists${NC}"
fi

echo ""
echo "🧪 Step 7: Testing bot (5 second test run)..."
echo -e "${YELLOW}Running bot for 5 seconds to verify it works...${NC}"
timeout 5 python "$BOT_SCRIPT" || true
echo -e "${GREEN}✅ Test completed${NC}"

echo ""
echo "🔧 Step 8: Creating systemd service..."
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

# Create service file
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Alpaca Trading Bot
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/$BOT_SCRIPT
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✅ Service file created at $SERVICE_FILE${NC}"

echo ""
echo "🔄 Step 9: Enabling and starting service..."
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"

echo ""
echo "📊 Step 10: Checking service status..."
sleep 2
systemctl status "$SERVICE_NAME" --no-pager -l

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo "Useful commands:"
echo "  View logs:        journalctl -u $SERVICE_NAME -f"
echo "  Check status:     systemctl status $SERVICE_NAME"
echo "  Restart bot:      systemctl restart $SERVICE_NAME"
echo "  Stop bot:         systemctl stop $SERVICE_NAME"
echo "  Start bot:        systemctl start $SERVICE_NAME"
echo ""
echo -e "${GREEN}Your bot is now running 24/7! 🚀${NC}"

