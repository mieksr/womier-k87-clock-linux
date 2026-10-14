#!/bin/sh
# Remove everything install.sh added.
set -eu
[ "$(id -u)" -eq 0 ] || { echo "Run as root: sudo $0" >&2; exit 1; }
PREFIX=${PREFIX:-/usr/local}
rm -f "$PREFIX/bin/womier-clock-sync" \
      /etc/udev/rules.d/70-womier-clock.rules \
      /etc/systemd/system/womier-clock-sync.service
systemctl daemon-reload
udevadm control --reload
echo "Removed."
