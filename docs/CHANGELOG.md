# Changelog

## [1.2.0] - 2026-03-20
### Added
- **Per-Folder Version Memory**: App now remembers the last version text for each folder path 📁
- **Auto-Fill Version Field**: Version field automatically populates when a folder is selected ✨

### Fixed
- **Folder Selection Persistence**: Fixed issue where folder selection was lost when editing the version text field. Both widgets now maintain independent selections. ✅

## [1.1.0] - 2026-03-17
### Added
- **Green Progress Bar**: Progress bar now has a stylish green color. 🟢
- **Larger Default Viewport**: Increased window size to 700x600. 📐
- **Version Display**: Version number clearly displayed in the app title.

## [1.0] - 2026-03-14

### Added
- **Professional App Icon** (1024x1024 PNG)
  - Blue gradient folder with zipper design
  - Embedded in Windows and Linux executables

- **Support & Feedback Section** in UI with:
  - Buy Me a Coffee donation button
  - PayPal Donate button
  - GitHub Issues link for bug reports and feature requests

- **Linux Packaging Support**:
  - Debian/Ubuntu (.deb) packages
  - Arch Linux (.pkg.tar.zst) packages
  - RPM (Fedora/RHEL) packages
  - Build scripts for all platforms

### Fixed
- **Startup Directory**: EXE now starts in executable's directory instead of %APPDATA%\Local\Temp
- Detection of PyInstaller frozen state using `sys.frozen`
- Proper working directory set for compiled executables

### Changed
- Version numbering reset to 1.0 for official release
- Enhanced build.py with multi-platform support
- Updated all documentation with Linux instructions

### Technical
- Added webbrowser module for opening links
- New methods: open_coffee_link(), open_paypal_link(), open_github_issues()
