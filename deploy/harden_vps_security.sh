#!/bin/bash
# =============================================================================
# Supreme Feng Shui AGI - Production VPS Security Hardening Script
# Hardens Google Cloud VPS: UFW Firewall, Fail2ban, Kernel TCP Shield,
# File Permissions (.env 600), Systemd Sandboxing & Anti-DDoS Protections.
# =============================================================================

set -e

echo "============================================================"
echo "🛡️  Supreme Feng Shui AGI - VPS Security Hardening Utility"
echo "============================================================"

# 1. Update Packages and Install Essential Security Tools
echo "📦 [1/6] Installing Security Packages (UFW, Fail2ban, iptables)..."
sudo apt-get update -qq
sudo apt-get install -y -qq ufw fail2ban iptables-persistent

# 2. Configure UFW Firewall
echo "🔥 [2/6] Configuring UFW Firewall Rules..."
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp comment 'SSH Secure Access'
sudo ufw allow 80/tcp comment 'HTTP Web Port'
sudo ufw allow 443/tcp comment 'HTTPS Secure Web Port'
sudo ufw allow 8000/tcp comment 'Supreme Feng Shui REST API'

# Enable UFW without prompting
echo "y" | sudo ufw enable
sudo ufw status verbose

# 3. Configure Fail2ban for SSH & Brute-Force Defense
echo "🛡️ [3/6] Setting up Fail2ban Intrusion Prevention..."
sudo tee /etc/fail2ban/jail.local > /dev/null << 'EOF'
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 5
banaction = ufw

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 4
EOF

sudo systemctl restart fail2ban
sudo systemctl enable fail2ban

# 4. Kernel Network Security & TCP SYN Flood Shield
echo "🔒 [4/6] Applying Kernel TCP Shield & Anti-Spoofing Parameters..."
sudo tee /etc/sysctl.d/99-fengshui-security.conf > /dev/null << 'EOF'
# TCP SYN Flood Protection
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2

# IP Spoofing & Redirect Protection
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Ignore ICMP Broadcast Echoes (Anti Smurf Attack)
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.icmp_ignore_bogus_error_responses = 1

# Protect Memory from core dumps
fs.suid_dumpable = 0
EOF

sudo sysctl --system -q || true

# 5. Secure File Permissions (.env & Database)
echo "🔑 [5/6] Securing Sensitive File Permissions..."
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ -f "$APP_DIR/.env" ]; then
    chmod 600 "$APP_DIR/.env"
    echo "✓ Locked $APP_DIR/.env to chmod 600 (Owner Read/Write only)"
fi

if [ -f "$APP_DIR/data/supreme_fengshui.db" ]; then
    chmod 600 "$APP_DIR/data/supreme_fengshui.db"* 2>/dev/null || true
    echo "✓ Locked $APP_DIR/data/supreme_fengshui.db to chmod 600"
fi

# 6. Hardening Systemd Service
echo "⚙️ [6/6] Hardening systemd Service Sandboxing..."
SERVICE_FILE="/etc/systemd/system/fengshui.service"
if [ -f "$SERVICE_FILE" ]; then
    # Ensure systemd has security sandboxing flags
    if ! grep -q "NoNewPrivileges" "$SERVICE_FILE"; then
        sudo sed -i '/\[Service\]/a NoNewPrivileges=true\nPrivateTmp=true' "$SERVICE_FILE"
        sudo systemctl daemon-reload
        sudo systemctl restart fengshui
        echo "✓ Added NoNewPrivileges=true & PrivateTmp=true to systemd service"
    fi
fi

echo ""
echo "============================================================"
echo "✅ Supreme Feng Shui VPS Security Hardening Complete!"
echo "• UFW Firewall: ACTIVE (Ports 22, 80, 443, 8000 allowed)"
echo "• Fail2ban Shield: ACTIVE (Auto-bans brute force attacks)"
echo "• Kernel TCP Shield: ACTIVE (Anti-DDoS & SYN Flood Protection)"
echo "• Secrets: LOCKED (.env chmod 600)"
echo "============================================================"
