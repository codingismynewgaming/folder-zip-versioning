# Installation Guide

## Windows

### Prerequisites

- Windows 10/11
- Python 3.8+ (optional, for running from source)
- pip (optional, for running from source)

### Installation Options

#### Option 1: Download Executable (Recommended)

1. Download `FolderZipperVersioning.exe` from the `builds/` folder
2. Double-click to run

#### Option 2: Run from Source

1. Install Python from [python.org](https://python.org)
2. Clone or download repository
3. `pip install -r requirements.txt`
4. `python app-files/zipper.py`

#### Option 3: Build Executable

```bash
pip install pyinstaller
python build.py
```

---

## Linux

### Prerequisites

- Python 3.8+
- python3-tk (Tkinter)
- tkinter

### Installation Options

#### Option 1: Debian/Ubuntu (.deb package)

For Ubuntu 20.04+, Debian 10+, and derivatives:

```bash
# Install dependencies
sudo apt update
sudo apt install python3-tk

# Install the package
sudo dpkg -i builds/folder-zipper-versioning_1.0_all.deb

# Or use apt for automatic dependency resolution
sudo apt install ./builds/folder-zipper-versioning_1.0_all.deb
```

**Launch:** `folder-zipper-versioning` from terminal or Applications menu

#### Option 2: Arch Linux (.pkg.tar.zst)

For Arch Linux, Manjaro, EndeavourOS:

```bash
# Install dependencies
sudo pacman -S python python-tkinter tk

# Install the package
sudo pacman -U builds/folder-zipper-versioning-1.0-1-any.pkg.tar.zst
```

**Launch:** `folder-zipper-versioning` from terminal or Applications menu

#### Option 3: Fedora/RHEL (.rpm package)

For Fedora 35+, RHEL 8+, CentOS Stream:

```bash
# Install dependencies
sudo dnf install python3-tkinter tkinter

# Install the package
sudo dnf install builds/folder-zipper-versioning-1.0-1.noarch.rpm
```

**Launch:** `folder-zipper-versioning` from terminal or Applications menu

#### Option 4: Run from Source

```bash
# Install dependencies (Debian/Ubuntu)
sudo apt install python3 python3-tk python3-pip

# Install dependencies (Fedora)
sudo dnf install python3 python3-tkinter python3-pip

# Install dependencies (Arch)
sudo pacman -S python python-tkinter python-pip

# Clone and run
git clone <repository-url>
cd zip-folder-automation
python3 app-files/zipper.py
```

#### Option 5: Build Linux Executable

```bash
# Install PyInstaller
pip3 install pyinstaller

# Build
python3 build.py --executable

# Run
./builds/FolderZipperVersioning
```

#### Option 6: Build All Linux Packages (Linux only)

```bash
# Install build tools

# Debian/Ubuntu
sudo apt install dpkg-dev debhelper python3-setuptools

# Arch Linux
sudo pacman -S base-devel devtools

# Fedora/RHEL
sudo dnf install rpm-build rpmdevtools

# Build all packages
python3 build.py --all

# Or build specific packages
python3 build.py --deb    # Debian package only
python3 build.py --arch   # Arch package only
python3 build.py --rpm    # RPM package only
```

---

## macOS

macOS support is planned for future releases.

---

## Troubleshooting

### Tkinter not found (Linux)

**Debian/Ubuntu:**
```bash
sudo apt install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S python-tkinter
```

### Permission denied when running executable

```bash
chmod +x builds/FolderZipperVersioning
./builds/FolderZipperVersioning
```

### Desktop icon not showing

Run the following to refresh the desktop database:

```bash
update-desktop-database ~/.local/share/applications
gtk-update-icon-cache -f /usr/share/icons/hicolor
```

### Application won't start

Check if Python and Tkinter are properly installed:

```bash
python3 --version
python3 -c "import tkinter; print('Tkinter OK')"
```
