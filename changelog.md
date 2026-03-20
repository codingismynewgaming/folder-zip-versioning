# Changelog

## [1.2.0] - 2026-03-20
### Added
- **Per-Folder Version Memory**: App now remembers the last version text for each folder path 📁
- **Auto-Fill Version Field**: Version field automatically populates when a folder is selected ✨
- **Config Migration**: Seamless migration from single `last_version` to `folder_versions` dict 🔄
- **Comprehensive Test Suite**: 39 unit tests with mocked filesystem and I/O 🧪

### Changed
- **Config Structure**: Changed from `{ "last_version": "..." }` to `{ "folder_versions": { "path": "version" } }`
- **UI Behavior**: Single-click on folder now shows stored version in status label
- **Thread Safety**: Combined `root.after()` calls to prevent race conditions in background thread

### Fixed
- **Race Condition**: Fixed potential UI update ordering issue in zipping thread finally block
- **Path Handling**: Documented path normalization edge case for future improvement
- **Folder Selection**: Fixed folder unselecting when editing version field - now persists selection ✅

### Technical
- **New Methods**: `get_folder_version()`, `save_folder_version()`, `save_config_from_dict()`
- **Migration Logic**: Old `last_version` preserved as `__default__` fallback for backward compatibility
- **Code Review**: Passed final quality gate with 0 Critical, 2 Major (fixed), 4 Minor findings
- **Bug Fix**: `self.selected_folder` now populated and used for zipping operation

---
*Major feature release: Per-folder version memory with full test coverage.*

## [1.1.0] - 2026-03-17
### Added
- **Green Progress Bar**: Progress bar now has a stylish green color. 🟢
- **Larger Default Viewport**: Increased window size to 700x600 to prevent bottom-cut issues. 📐
- **Version Display**: Version number clearly displayed in the app title.

### Fixed
- Fixed "attribute error" for human-readable size conversion.
- Optimized UI layout for better spacing with the new progress bar.

---
*Bumping version to 1.1 with UI refinements and green theme.*
