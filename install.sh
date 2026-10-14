#!/bin/sh
# Install womier-clock-sync, its udev rule and the plug-in auto-sync service.
# Usage: sudo ./install.sh            (installs under /usr/local)
#        sudo PREFIX=/usr ./install.sh
set -eu
[ "$(id -u)" -eq 0 ] || { echo "Run as root: sudo $0" >&2; exit 1; }
here=$(cd "$(dirname "$0")" && pwd)
PREFIX=${PREFIX:-/usr/local}

install -Dm755 "$here/womier-clock-sync" "$PREFIX/bin/womier-clock-sync"
install -Dm644 "$here/70-womier-clock.rules" /etc/udev/rules.d/70-womier-clock.rules
sed "s|/usr/bin/womier-clock-sync|$PREFIX/bin/womier-clock-sync|" "$here/womier-clock-sync.service" \
    > /etc/systemd/system/womier-clock-sync.service
chmod 644 /etc/systemd/system/womier-clock-sync.service

systemctl daemon-reload
udevadm control --reload
# Apply to a keyboard that is already plugged in
udevadm trigger --action=add --subsystem-match=usb --attr-match=idVendor=0c45 --attr-match=idProduct=800b

echo "Installed. Plug the keyboard in (wired mode) or run: womier-clock-sync"
