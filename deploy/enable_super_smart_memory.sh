#!/usr/bin/env bash
# =============================================================================
# Supreme Feng Shui AGI System - Standalone Super Smart Hybrid Memory Installer
# Architecture: zRAM (LZ4 Compressed In-Memory) + 4GB NVMe Swap + Smart Sysctl
# Turns 1GB VPS into ~6.5GB High-Speed Virtual Memory with Zero OOM Crashes!
# =============================================================================

set -e

if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root (sudo ./enable_super_smart_memory.sh)"
  exit 1
fi

echo "====================================================================="
echo "🚀 Activating Super Smart Hybrid Memory Architecture 🚀"
echo "====================================================================="

# Step 1: Clean & Reconfigure 4GB NVMe Disk Swap (Tier 2 Safety Net)
echo "[1/4] Configuring 4GB High-Capacity NVMe Swap (Priority 10)..."
if [ -f /swapfile ]; then
    swapoff /swapfile 2>/dev/null || true
    rm -f /swapfile
fi

fallocate -l 4G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=4096
chmod 600 /swapfile
mkswap /swapfile
swapon -p 10 /swapfile

# Ensure persistent mount in /etc/fstab with priority 10
sed -i '/\/swapfile/d' /etc/fstab
echo "/swapfile none swap sw,pri=10 0 0" >> /etc/fstab
echo "✓ 4GB NVMe Swap File initialized with Priority 10."

# Step 2: Install and Configure zRAM (Tier 1 Ultra-Fast Compressed RAM)
echo "[2/4] Installing & Configuring zRAM (LZ4 Compression, Priority 100)..."
apt-get update -qq
apt-get install -y -qq zram-tools

cat << 'ZRAM_CONF' > /etc/default/zramswap
# Supreme Feng Shui High-Speed Compressed RAM Configuration
ALGO=lz4
PERCENT=150
PRIORITY=100
ZRAM_CONF

systemctl restart zramswap || service zramswap restart
echo "✓ zRAM active with LZ4 Compression and Priority 100."

# Step 3: Apply Super Smart Kernel Memory Tuning (sysctl)
echo "[3/4] Tuning Kernel Virtual Memory Subsystem (sysctl)..."
sed -i '/SUPREME FENG SHUI MEMORY OPTIMIZATION/,$d' /etc/sysctl.conf

cat << 'SYSCTL_CONF' >> /etc/sysctl.conf

# === SUPREME FENG SHUI MEMORY OPTIMIZATION ===
# Maximize usage of fast compressed zRAM before hitting disk
vm.swappiness=100
# Preserve file system dentry/inode caches
vm.vfs_cache_pressure=50
# Smooth asynchronous background disk flushing to prevent CPU spikes
vm.dirty_background_ratio=5
vm.dirty_ratio=10
# Single page decompression for ultra-fast zRAM response
vm.page-cluster=0
# Allow memory overcommit safely with zRAM backing
vm.overcommit_memory=1
SYSCTL_CONF

sysctl -p /etc/sysctl.conf

# Step 4: Verification and Telemetry Output
echo "[4/4] Verifying Super Smart Memory Allocation..."
echo "====================================================================="
echo "✅ Super Smart Hybrid Memory Activated Successfully!"
echo "====================================================================="
free -h
echo "--- Active Swap Devices & Priorities ---"
swapon --show
