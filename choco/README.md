# Chocolatey Package Directory
# This folder contains files for creating Chocolatey packages

# The package is automatically built by GitHub Actions workflow
# Files needed:
# - folderzipper-versioning.nuspec (package manifest)
# - tools/chocolateyInstall.ps1 (installation script)
# - tools/chocolateyUninstall.ps1 (uninstallation script)

# Manual build (if needed):
# 1. Install Chocolatey: https://chocolatey.org/install
# 2. Run: choco pack folderzipper-versioning.nuspec
# 3. Test: choco install folderzipper-versioning -s .
# 4. Push: choco push folderzipper-versioning.*.nupkg --source https://push.chocolatey.org/

# For automated builds, see: .github/workflows/chocolatey.yml
