# Changelog

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
