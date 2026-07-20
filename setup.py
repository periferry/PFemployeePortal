import os
import sys
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

def get_asset_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def create_shortcut(target_path, shortcut_path, working_dir):
    ps_command = f"""
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
    $Shortcut.TargetPath = "{target_path}"
    $Shortcut.WorkingDirectory = "{working_dir}"
    $Shortcut.IconLocation = "{target_path},0"
    $Shortcut.Save()
    """
    # Replace backslashes with double backslashes for PowerShell compatibility
    ps_command = ps_command.replace('\\', '\\\\')
    subprocess.run(["powershell", "-Command", ps_command], capture_output=True)

class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PeriFerry Employee Portal Setup")
        self.root.geometry("450x320")
        self.root.resizable(False, False)
        self.root.configure(bg="#070c1e")
        
        # Center Window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 450) // 2
        y = (screen_height - 320) // 2
        self.root.geometry(f"+{x}+{y}")

        # Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TProgressbar", thickness=15, troughcolor="#0e1938", background="#5046b6")
        
        # UI Elements
        # 1. Company Logo Graphic
        try:
            logo_path = get_asset_path('logo.png')
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                # Automatically crop transparent padding borders
                bbox = img.getbbox()
                if bbox:
                    img = img.crop(bbox)
                # Resize keeping aspect ratio to look perfect in the wizard header
                img.thumbnail((360, 90), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img)
                self.logo_label = tk.Label(root, image=self.logo_img, bg="#070c1e")
                self.logo_label.pack(pady=(20, 5))
            else:
                self.fallback_title()
        except Exception:
            self.fallback_title()
            
        # 2. Main Subtitle
        self.subtitle_label = tk.Label(
            root, 
            text="Pre-configuring spreadsheet database and preparing workspace...", 
            font=("Poppins", 9), 
            bg="#070c1e", 
            fg="#94a3b8"
        )
        self.subtitle_label.pack(pady=5)
        
        # 3. Status text
        self.status_label = tk.Label(
            root, 
            text="Ready to install the Employee Portal", 
            font=("Poppins", 9), 
            bg="#070c1e", 
            fg="#cbd5e1"
        )
        self.status_label.pack(pady=(25, 5))
        
        # 4. Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=360, mode="determinate")
        self.progress.pack(pady=5)
        
        # 5. Buttons
        self.btn_frame = tk.Frame(root, bg="#070c1e")
        self.btn_frame.pack(pady=(20, 10))
        
        self.install_btn = tk.Button(
            self.btn_frame, 
            text="Install Now", 
            font=("Poppins", 10, "bold"),
            bg="#5046b6", 
            fg="#ffffff", 
            activebackground="#c8469e", 
            activeforeground="#ffffff",
            bd=0, 
            padx=20, 
            pady=8,
            command=self.start_installation
        )
        self.install_btn.pack()

    def fallback_title(self):
        self.title_label = tk.Label(
            self.root, 
            text="PeriFerry Employee Portal", 
            font=("Poppins", 16, "bold"), 
            bg="#070c1e", 
            fg="#ffffff"
        )
        self.title_label.pack(pady=(25, 5))

    def update_status(self, text, val):
        self.status_label.config(text=text)
        self.progress['value'] = val
        self.root.update()

    def start_installation(self):
        self.install_btn.config(state="disabled")
        try:
            # 1. Create directory
            self.update_status("Creating installation folder...", 20)
            install_dir = os.path.join(os.environ['LOCALAPPDATA'], 'PeriFerry Employee Portal')
            os.makedirs(install_dir, exist_ok=True)
            
            # 2. Extract exe
            self.update_status("Copying application binaries...", 45)
            src_exe = get_asset_path('PeriFerry Employee Portal.exe')
            dest_exe = os.path.join(install_dir, 'PeriFerry Employee Portal.exe')
            shutil.copy2(src_exe, dest_exe)
            
            # 3. Extract config
            self.update_status("Pre-configuring database URL...", 65)
            src_config = get_asset_path('config.json')
            dest_config = os.path.join(install_dir, 'config.json')
            shutil.copy2(src_config, dest_config)
            
            # 4. Create Desktop shortcut
            self.update_status("Creating Desktop shortcut...", 85)
            desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            desktop_shortcut = os.path.join(desktop_path, 'PeriFerry Employee Portal.lnk')
            create_shortcut(dest_exe, desktop_shortcut, install_dir)
            
            # 5. Create Start Menu shortcut
            self.update_status("Creating Start Menu shortcut...", 95)
            start_menu_path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')
            start_menu_shortcut = os.path.join(start_menu_path, 'PeriFerry Employee Portal.lnk')
            create_shortcut(dest_exe, start_menu_shortcut, install_dir)
            
            # Done!
            self.update_status("Installation complete!", 100)
            messagebox.showinfo("Success", "PeriFerry Employee Portal installed successfully!\n\nA shortcut has been created on your Desktop.")
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during installation:\n{str(e)}")
            self.install_btn.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = InstallerApp(root)
    root.mainloop()
