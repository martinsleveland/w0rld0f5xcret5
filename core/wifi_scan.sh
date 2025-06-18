#!/bin/bash

IFACE="$1"
OUT="scan_results"

if [[ $EUID -ne 0 ]]; then
    echo "[!] Run as root!"
    exit 1
fi

sudo airmon-ng start "$IFACE" >/dev/null 2>&1
MON_IFACE="${IFACE}mon"

timeout 6s sudo airodump-ng "$MON_IFACE" --output-format csv -w "$OUT" >/dev/null 2>&1

sudo airmon-ng stop "$MON_IFACE" >/dev/null 2>&1

echo "Saving file..."
echo "$OUT-01.csv"
