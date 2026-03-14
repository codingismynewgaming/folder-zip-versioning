# Changelog

## [1.0.1] - 2026-03-14

### Added
- App icon (512x512 PNG) embedded in executables
- Linux packaging support:
  - Debian/Ubuntu (.deb) packages
  - Arch Linux (.pkg.tar.zst) packages
  - RPM (Fedora/RHEL) packages
- Build script enhancements:
  - `--deb`, `--arch`, `--rpm`, `--all` flags
  - Automatic icon detection and embedding
  - Overwrite handling for rebuilds

### Fixed
- **Startup Directory**: EXE now starts in executable's directory instead of %APPDATA%\Local\Temp
- Detection of PyInstaller frozen state using `sys.frozen`
- Proper working directory set for compiled executables

### Changed
- Updated README.md with Linux installation instructions
- Enhanced build.py for cross-platform support
- Improved status documentation

### Technical
- Added PIL/Pillow for icon generation
- Created create_icon.py for automated icon creation
- Added desktop file integration for Linux GUI apps

---

## [1.0.0] - 2026-03-14

### Added
- Initial release
- Folder selection GUI with Tkinter
- Auto version numbering (001, 002, 003...)
- Custom version input field
- Timestamp in zip filenames
- Dark mode support for Windows
- Directory navigation (up/down)
- Real-time status feedback
- Test suite for versioning logic

### Technical
- Pure Python standard library
- No external dependencies required
- PyInstaller build script included

### Known Issues
- None reported
