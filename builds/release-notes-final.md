## 🎉 FolderZipperVersioning v1.0 - Official Release

### ✨ Features
- 📦 Zip folders with automatic version numbering
- 🔢 Custom version input field (e.g., 1.0.1)
- ⏱️ Timestamp in filename
- 🌓 Dark mode support for Windows
- 📁 Built-in folder browser with navigation
- 🎨 Professional app icon (1024x1024)
- 💝 Support section with donation links
- 🐛 Direct GitHub Issues link for feedback

### 🛠️ Technical Fixes
- Fixed startup directory issue (no more AppData/Temp)
- Executable now starts in its own directory
- Professional gradient icon with zipper design

### 📦 Installation

**Windows:**
- Download `FolderZipperVersioning.exe` and run it

**Linux - Build from Source:**

1. Download `folder-zipper-versioning-1.0-source.tar.gz`
2. Extract: `tar -xzf folder-zipper-versioning-1.0-source.tar.gz`
3. Install dependencies for your distro:

   **Debian/Ubuntu:**
   ```bash
   sudo apt-get install python3-pil python3-tk dpkg-dev
   ./build-linux.sh --deb
   sudo dpkg -i builds/folder-zipper-versioning_1.0_all.deb
   ```

   **Arch Linux:**
   ```bash
   sudo pacman -S python-pillow python-tkinter base-devel
   cd arch-linux && makepkg -si
   ```

   **Fedora/RHEL:**
   ```bash
   sudo dnf install python3-pillow python3-tkinter rpm-build
   ./build-linux.sh --rpm
   sudo dnf install builds/folder-zipper-versioning-1.0.noarch.rpm
   ```

**Run without installing:**
```bash
python3 app-files/zipper.py
```

### 🤖 Automatic Package Builds

Linux packages will be automatically built and attached to this release using GitHub Actions. Check the "Assets" section above for:
- `.deb` package (Debian/Ubuntu)
- `.rpm` package (Fedora/RHEL)
- `.pkg.tar.zst` package (Arch Linux)

If packages aren't available yet, they're being built automatically. Check the Actions tab for build progress.

### 💝 Support the Project
- Buy Me a Coffee: https://buymeacoffee.com/codingiymynewgaming
- PayPal: https://www.paypal.com/donate/?hosted_button_id=ZXHJFTUW9NQK8

### 📋 Files in This Release
- `FolderZipperVersioning.exe` - Windows executable (11.5 MB)
- `folder-zipper-versioning-1.0-source.tar.gz` - Linux source distribution with packaging files

---
**Full Changelog:** https://github.com/codingismynewgaming/folder-zip-versioning/blob/main/docs/CHANGELOG.md
**GitHub Issues:** https://github.com/codingismynewgaming/folder-zip-versioning/issues
