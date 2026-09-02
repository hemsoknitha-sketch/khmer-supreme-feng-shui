#!/bin/bash
# =============================================================================
# Supreme Feng Shui AGI - VPS Disk Auto-Expansion Script (10GB -> 30GB+)
# Expands root partition & filesystem to utilize 100% of Google Cloud Disk Space
# =============================================================================

echo "============================================================"
echo "⚡ Supreme Feng Shui AGI - Disk Auto-Expansion Utility"
echo "============================================================"

# Check current disk space before expansion
echo "📊 Current Disk Usage Before Expansion:"
df -h /

# Install cloud-guest-utils (growpart) if not present
if ! command -v growpart &> /dev/null; then
    echo "📦 Installing cloud-guest-utils..."
    sudo apt-get update -qq && sudo apt-get install -y -qq cloud-guest-utils
fi

# Detect root partition and disk
ROOT_PART=$(df / | tail -1 | awk '{print $1}')
echo "🔍 Detected Root Partition: $ROOT_PART"

# Handle standard sda1, vda1, nvme0n1p1
if [[ "$ROOT_PART" =~ nvme[0-9]+n[0-9]+p[0-9]+ ]]; then
    DISK_DEV=$(echo "$ROOT_PART" | sed -E 's/p[0-9]+$//')
    PART_NUM=$(echo "$ROOT_PART" | grep -o -E '[0-9]+$')
    echo "🔧 Expanding NVMe partition: $DISK_DEV partition $PART_NUM"
    sudo growpart "$DISK_DEV" "$PART_NUM" 2>/dev/null || true
    sudo resize2fs "$ROOT_PART" 2>/dev/null || sudo xfs_growfs / 2>/dev/null || true
elif [[ "$ROOT_PART" =~ [a-z]+[0-9]+ ]]; then
    DISK_DEV=$(echo "$ROOT_PART" | sed -E 's/[0-9]+$//')
    PART_NUM=$(echo "$ROOT_PART" | grep -o -E '[0-9]+$')
    echo "🔧 Expanding Partition: $DISK_DEV partition $PART_NUM"
    sudo growpart "$DISK_DEV" "$PART_NUM" 2>/dev/null || true
    sudo resize2fs "$ROOT_PART" 2>/dev/null || sudo xfs_growfs / 2>/dev/null || true
else
    echo "⚠️ Trying universal resize..."
    sudo resize2fs /dev/sda1 2>/dev/null || sudo resize2fs /dev/root 2>/dev/null || true
fi

echo ""
echo "============================================================"
echo "✅ Disk Expansion Complete! New Disk Usage:"
echo "============================================================"
df -h /
