# Changelog

## [1.1.0] - 2026-03-16
### Added
- **Version Persistence**: App now remembers your last entered version number even after closing and reopening.
- **Improved UI**: Version input field moved next to the Zip button for better visibility and accessibility.
- **Config File**: Settings saved to `folderzipperconfig.json` next to the executable.

### Changed
- Version input field is now more prominent with bold label.
- Config file renamed to `folderzipperconfig.json` for clarity.

### Fixed
- Config file path now correctly saves next to the executable in builds folder, not in bundled app-files.

### Technical
- Updated Linux package workflows (Debian, Arch, RPM) to version 1.1.
- Chocolatey and WinGet workflows configured for automated releases.

## [1.0.1] - 2026-03-15
### Fixed
- GitHub Actions workflows for Linux packages (Debian, Arch, RPM) now use native container-based builds for better reliability.
- Fixed Arch Linux dependency build error by swapping non-existent `python-tkinter` with `tk`.
- Fixed RPM package build by using a Fedora container and installing `python3-devel` and `rpm-build`.
- Fixed release upload failure on manual runs by using GitHub Artifacts for `workflow_dispatch` and limiting release uploads to actual tag releases.
- Missing RPM spec file in repository.
- Arch Linux source file preparation.
- Unnecessary Pillow/PIL dependencies removed from all Linux packages.
- Standardized application and file naming across all Linux distributions.
- Standardized icons for all builds.

## [1.0.0] - 2026-03-14
### Added
- Initial release of Folder Zipper with Versioning.
- Auto-incrementing version numbering.
- Custom version support.
- GUI for easy folder selection.
- Dark mode support.
- Support for Debian, Arch, and RPM builds.
