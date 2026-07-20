import os
import sys
import subprocess

def install_and_import(package, import_name=None):
    if import_name is None:
        import_name = package
    try:
        __import__(import_name)
        print(f"'{import_name}' is already installed.")
    except ImportError:
        print(f"Installing '{package}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed '{package}'.")

def main():
    # 1. Ensure required build tools are installed
    install_and_import("Pillow", "PIL")
    install_and_import("pyinstaller")
    
    # Paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "PERIFERRY LOGO PACKAGE", "PF PRIMARY LOGO", "DIGITAL", "PNG", "logo.png")
    icon_path = os.path.join(current_dir, "logo.ico")
    
    # 2. Create the .ico file from logo.png if it exists
    if os.path.exists(logo_path):
        try:
            from PIL import Image
            print(f"Converting logo from '{logo_path}' to icon '{icon_path}'...")
            img = Image.open(logo_path)
            # Save as ICO with multiple sizes for standard Windows display
            img.save(icon_path, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
            print("Successfully created 'logo.ico' icon file.")
        except Exception as e:
            print(f"Warning: Could not create logo.ico: {e}")
            icon_path = None
    else:
        print(f"Warning: Logo file not found at '{logo_path}'. Building without custom icon.")
        icon_path = None

    # 3. Assemble PyInstaller command
    pyinstaller_cmd = [
        "pyinstaller",
        "--noconsole",
        "--onefile",
        "--add-data", "index.html;.",
        "--name", "PeriFerry Employee Portal",
        "app.py"
    ]
    
    # Append icon if created successfully
    if icon_path and os.path.exists(icon_path):
        pyinstaller_cmd.extend(["--icon", "logo.ico"])
        
    print(f"Running PyInstaller command: {' '.join(pyinstaller_cmd)}")
    
    # 4. Execute build process
    try:
        subprocess.check_call(pyinstaller_cmd, cwd=current_dir)
        print("\n" + "="*50)
        print("BUILD COMPLETED SUCCESSFULY!")
        print("Your executable can be found in:")
        print(os.path.join(current_dir, "dist", "PeriferryTracker.exe"))
        print("="*50)
    except subprocess.CalledProcessError as e:
        print(f"Error: PyInstaller build failed with exit code {e.returncode}")
        sys.exit(1)

if __name__ == '__main__':
    main()
