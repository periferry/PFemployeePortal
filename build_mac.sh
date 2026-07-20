#!/bin/bash
# Shell helper to build macOS app & DMG installer
set -e

echo "=== PeriFerry Employee Portal macOS Build ==="
python3 -m pip install --upgrade pip
python3 -m pip install requests pywebview pyinstaller pillow pyobjc-framework-Cocoa pyobjc-framework-WebKit

python3 build_mac.py
