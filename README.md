# FolderZipperVersioning

A Python Tkinter GUI application that zips folders with automatic version numbering.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux-lightgrey.svg)

## Features

- 📁 Easy Folder Selection via GUI
- 🔢 Auto Version Numbering (001, 002, 003...)
- ✏️ Custom Version Input
- 🕐 Timestamp in filenames
- 🌙 Dark Mode Support (Windows)
- 📂 Directory Navigation
- 🐧 Linux Package Support (deb, pkg.tar.zst, rpm)

## Screenshots

![App Icon](app-files/icon.png)

## Installation

### Windows

**Download Executable:**
```bash
# Download FolderZipperVersioning.exe from builds/ folder
# Double-click to run
```

**Or run from source:**
```bash
pip install -r requirements.txt
python app-files/zipper.py
```

### Linux

**Ubuntu/Debian:**
```bash
sudo apt install ./builds/folder-zipper-versioning_1.0_all.deb
folder-zipper-versioning
```

**Arch Linux:**
```bash
sudo pacman -U builds/folder-zipper-versioning-1.0-1-any.pkg.tar.zst
folder-zipper-versioning
```

**Fedora/RHEL:**
```bash
sudo dnf install builds/folder-zipper-versioning-1.0-1.noarch.rpm
folder-zipper-versioning
```

**Or run from source:**
```bash
sudo apt install python3-tk  # Debian/Ubuntu
python3 app-files/zipper.py
```

📖 See [docs/INSTALL.md](docs/INSTALL.md) for detailed installation instructions.

## Usage

1. Launch the application
2. Navigate to the folder you want to zip
3. (Optional) Enter a custom version number
4. Click "Zip Selected Folder"
5. The zip file is created in the parent directory with format:
   - Auto-version: `foldername_001_2026-03-14_16-30.zip`
   - Custom version: `1.0-foldername_2026-03-14_16-30.zip`

📖 See [docs/USAGE.md](docs/USAGE.md) for detailed usage guide.

## Building

### Windows

```bash
python build.py
# Output: builds/FolderZipperVersioning.exe
```

### Linux

**Build executable:**
```bash
python3 build.py --executable
# Output: builds/FolderZipperVersioning
```

**Build all packages:**
```bash
python3 build.py --all
# Output: builds/*.deb, builds/*.pkg.tar.zst, builds/*.rpm
```

**Build specific package:**
```bash
python3 build.py --deb    # Debian package
python3 build.py --arch   # Arch package
python3 build.py --rpm    # RPM package
```

## Project Structure

```
zip-folder-automation/
├── app-files/
│   ├── zipper.py          # Main application
│   ├── test_zipper.py     # Unit tests
│   └── icon.png           # Application icon
├── builds/
│   ├── FolderZipperVersioning.exe  # Windows executable
│   ├── FolderZipperVersioning      # Linux executable
│   ├── *.deb                       # Debian package
│   ├── *.pkg.tar.zst               # Arch package
│   └── *.rpm                       # RPM package
├── debian/                 # Debian packaging files
├── arch-linux/             # Arch packaging files
├── rpm/                    # RPM packaging files
├── docs/
│   ├── INSTALL.md          # Installation guide
│   ├── USAGE.md            # Usage guide
│   ├── FEATURES.md         # Feature documentation
│   └── CHANGELOG.md        # Version history
├── internals/              # Secrets and sensitive files (not in git)
├── build.py                # Build script
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Support

- 📖 [Usage Guide](docs/USAGE.md)
- 📦 [Installation Guide](docs/INSTALL.md)
- 🐛 [Report Issues](https://github.com/yourusername/folder-zipper-versioning/issues)
