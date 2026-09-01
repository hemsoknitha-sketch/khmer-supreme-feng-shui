#!/usr/bin/env bash
# =============================================================================
# Supreme Feng Shui AGI System - 1GB VPS Automated Setup Script
# Features: Super Smart Hybrid Memory (zRAM + 4GB NVMe Swap + Smart Sysctl)
# Turns 1GB VPS into ~6.5GB High-Speed Virtual Memory with Zero OOM Crashes!
# =============================================================================

set -e

echo "====================================================================="
echo "🌟 Setting up Supreme Feng Shui AGI System on 1GB RAM VPS 🌟"
echo "====================================================================="

# 1. Configure Super Smart Hybrid Memory (zRAM + 4GB Swap)
echo "[1/6] Configuring Super Smart Hybrid Memory (zRAM + 4GB NVMe Swap)..."
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ -f "$PROJECT_DIR/deploy/enable_super_smart_memory.sh" ]; then
    chmod +x "$PROJECT_DIR/deploy/enable_super_smart_memory.sh"
    bash "$PROJECT_DIR/deploy/enable_super_smart_memory.sh"
else
    # Fallback inline swap
    fallocate -l 4G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=4096
    chmod 600 /swapfile
    mkswap /swapfile
    swapon -p 10 /swapfile || swapon /swapfile
fi

# 2. Update system packages and install Python 3 & pip
echo "[2/6] Installing Python runtime and core dependencies..."
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv git curl

# 3. Create Virtual Environment
echo "[3/6] Creating Python virtual environment..."
cd "$PROJECT_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 4. Install lightweight production requirements
echo "[4/6] Installing lightweight production requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Configure Environment file if missing
echo "[5/6] Checking environment file (.env)..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️ Created .env from .env.example. Remember to edit .env and put your actual tokens!"
fi

# 6. Install and Start Systemd Service
echo "[6/6] Installing Systemd 24/7 background service..."
cp deploy/fengshui.service /etc/systemd/system/fengshui.service
sed -i "s|/root/Supreme_FengShui|$PROJECT_DIR|g" /etc/systemd/system/fengshui.service
sed -i "s|/usr/bin/python3|$PROJECT_DIR/venv/bin/python|g" /etc/systemd/system/fengshui.service

systemctl daemon-reload
systemctl enable fengshui
systemctl restart fengshui

echo "====================================================================="
echo "✅ Setup Complete! Supreme Feng Shui AGI is now running 24/7."
echo "Status check: systemctl status fengshui"
echo "Web UI: http://YOUR_VPS_IP:8000"
echo "====================================================================="
