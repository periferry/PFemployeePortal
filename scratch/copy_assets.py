import os
import shutil

src_dir = r"C:\Users\vijay\AppData\Local\Temp" # Wait, the appDataDir has it.
# The artifacts are listed in: C:\Users\vijay\.gemini\antigravity\brain\8b2e8ef6-74a5-4baa-98b9-33ea1d33be89
artifacts_dir = r"C:\Users\vijay\.gemini\antigravity\brain\8b2e8ef6-74a5-4baa-98b9-33ea1d33be89"
dest_dir = r"c:\D Drive\Task Tracking\manual_assets"

os.makedirs(dest_dir, exist_ok=True)

# Copy all png files
for filename in os.listdir(artifacts_dir):
    if filename.endswith(".png"):
        shutil.copy2(os.path.join(artifacts_dir, filename), os.path.join(dest_dir, filename))
        print(f"Copied {filename} to manual_assets")
