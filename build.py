"""Build script for FolderZipperVersioning"""
import subprocess
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, "app-files")
BUILD_DIR = os.path.join(BASE_DIR, "builds")

def build():
    os.makedirs(BUILD_DIR, exist_ok=True)
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "FolderZipperVersioning",
        "--icon", "NONE",
        "--add-data", "app-files;app-files",
        os.path.join(APP_DIR, "zipper.py")
    ]
    
    print("Building FolderZipperVersioning...")
    subprocess.run(cmd, check=True)
    
    # Move executable to builds folder
    dist_exe = os.path.join(BASE_DIR, "dist", "FolderZipperVersioning.exe")
    if os.path.exists(dist_exe):
        shutil.move(dist_exe, BUILD_DIR)
        print(f"Executable created: {os.path.join(BUILD_DIR, 'FolderZipperVersioning.exe')}")
    
    # Cleanup
    for folder in ["build", "dist"]:
        path = os.path.join(BASE_DIR, folder)
        if os.path.exists(path):
            shutil.rmtree(path)
    
    print("Build complete!")

if __name__ == "__main__":
    build()
