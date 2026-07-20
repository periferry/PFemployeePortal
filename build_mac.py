#!/usr/bin/env python3
"""
PeriFerry Employee Portal - macOS Build & Installer Package Creator
-------------------------------------------------------------------
This script compiles the Python/PyWebView application into a native macOS app bundle
('PeriFerry Employee Portal.app') and packages it into a standard macOS DMG installer
('PeriFerry Employee Portal.dmg').

Usage (Run on macOS):
    python3 build_mac.py
"""

import os
import sys
import subprocess
import shutil

def install_and_import(package, import_name=None):
    if import_name is None:
        import_name = package
    try:
        __import__(import_name)
    except ImportError:
        print(f"Installing missing build dependency '{package}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def convert_png_to_icns(png_path, icns_path):
    """Converts a PNG image into a macOS .icns file format."""
    try:
        from PIL import Image
        img = Image.open(png_path)
        
        # Create iconset directory for iconutil if available
        iconset_dir = "logo.iconset"
        os.makedirs(iconset_dir, exist_ok=True)
        
        sizes = [16, 32, 64, 128, 256, 512]
        for s in sizes:
            resized = img.resize((s, s), Image.Resampling.LANCZOS)
            resized.save(os.path.join(iconset_dir, f"icon_{s}x{s}.png"))
            resized_2x = img.resize((s*2, s*2), Image.Resampling.LANCZOS)
            resized_2x.save(os.path.join(iconset_dir, f"icon_{s}x{s}@2x.png"))
            
        if shutil.which("iconutil"):
            subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", icns_path], check=True)
            shutil.rmtree(iconset_dir, ignore_errors=True)
            print(f"Successfully generated ICNS icon: {icns_path}")
            return icns_path
        else:
            shutil.rmtree(iconset_dir, ignore_errors=True)
    except Exception as e:
        print(f"Notice: ICNS generation skipped ({e}). PyInstaller will use standard assets.")
    return None

def main():
    print("=" * 60)
    print("      PERIFERRY EMPLOYEE PORTAL - MACOS BUILD SYSTEM       ")
    print("=" * 60)

    # Verify operating system
    if sys.platform != 'darwin':
        print("\n[!] WARNING: You are running this script on non-macOS platform (" + sys.platform + ").")
        print("    Apple macOS applications (.app / .dmg) MUST be compiled on a macOS system")
        print("    because PyInstaller creates native binaries for the host OS.")
        print("\n    Options to build the macOS package:")
        print("    1. Run this script directly on any Mac machine: 'python3 build_mac.py'")
        print("    2. Use GitHub Actions CI/CD workflow (included in .github/workflows/build-mac.yml)")
        print("    3. Run in a macOS Virtual Machine / Cloud Mac instance.")
        print("=" * 60)
        sys.exit(0)

    # 1. Install required python packages
    install_and_import("Pillow", "PIL")
    install_and_import("pyinstaller")
    install_and_import("pywebview")
    install_and_import("requests")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_png = os.path.join(current_dir, "PERIFERRY LOGO PACKAGE", "PF PRIMARY LOGO", "DIGITAL", "PNG", "logo.png")
    icns_path = os.path.join(current_dir, "logo.icns")

    # 2. Generate ICNS icon if logo PNG exists
    icon_file = None
    if os.path.exists(logo_png):
        icon_file = convert_png_to_icns(logo_png, icns_path)

    # 3. Assemble PyInstaller command for macOS
    # Path separator for --add-data is ':' on Unix/macOS
    cmd = [
        "pyinstaller",
        "--noconsole",
        "--windowed",
        "--add-data", f"{os.path.join(current_dir, 'index.html')}:.",
        "--name", "PeriFerry Employee Portal",
        "app.py"
    ]

    if os.path.exists(os.path.join(current_dir, "config.json")):
        cmd.extend(["--add-data", f"{os.path.join(current_dir, 'config.json')}:."])

    if icon_file and os.path.exists(icon_file):
        cmd.extend(["--icon", icon_file])

    print("\n[+] Compiling macOS Application Bundle (.app)...")
    print("    Running:", " ".join(cmd))
    subprocess.check_call(cmd, cwd=current_dir)

    app_path = os.path.join(current_dir, "dist", "PeriFerry Employee Portal.app")
    dmg_path = os.path.join(current_dir, "dist", "PeriFerry Employee Portal.dmg")

    if not os.path.exists(app_path):
        print("\n[!] Error: App bundle was not found at:", app_path)
        sys.exit(1)

    print("\n[✓] Created macOS App Bundle:", app_path)

    # 4. Create DMG Installer disk image using native macOS 'hdiutil' tool
    print("\n[+] Packaging into macOS DMG Installer Disk Image...")
    
    # Remove existing DMG if any
    if os.path.exists(dmg_path):
        os.remove(dmg_path)

    # Temporary staging folder for DMG
    dmg_stage = os.path.join(current_dir, "dist", "dmg_stage")
    if os.path.exists(dmg_stage):
        shutil.rmtree(dmg_stage)
    os.makedirs(dmg_stage)

    # Copy .app bundle to staging folder
    shutil.copytree(app_path, os.path.join(dmg_stage, "PeriFerry Employee Portal.app"))

    # Create symlink to /Applications inside DMG for easy Drag & Drop installation
    os.symlink("/Applications", os.path.join(dmg_stage, "Applications"))

    # Run hdiutil to create compressed DMG
    hdiutil_cmd = [
        "hdiutil", "create",
        "-volname", "PeriFerry Employee Portal",
        "-srcfolder", dmg_stage,
        "-ov",
        "-format", "UDZO",
        dmg_path
    ]

    try:
        subprocess.check_call(hdiutil_cmd)
        shutil.rmtree(dmg_stage)
        print("\n" + "=" * 60)
        print("          MACOS BUILD COMPLETED SUCCESSFULLY!          ")
        print("=" * 60)
        print("  macOS App Bundle :", app_path)
        print("  macOS DMG Package:", dmg_path)
        print("=" * 60)
    except Exception as e:
        print("\n[!] Warning: DMG creation failed:", e)
        print("    You can still use the .app bundle located in dist/ folder.")

if __name__ == "__main__":
    main()
