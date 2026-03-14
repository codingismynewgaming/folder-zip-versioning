# 📦 Publishing Guide - FolderZipperVersioning

## ✅ CI/CD Workflows Setup

All GitHub Actions workflows are configured for automatic publishing!

---

## 🔐 Secrets to Configure in GitHub

Go to: **GitHub Repo → Settings → Secrets and variables → Actions → New repository secret**

### Required Secrets:

| Secret Name | Value | How to Get |
|-------------|-------|------------|
| `CHOCOLATEY_API_KEY` | [Get from Chocolatey](https://community.chocolatey.org/account) | 1. Create account with jan.michael.kuehn.bln@gmail.com<br>2. Go to Account → API Key<br>3. Copy the key |
| `SNAPCRAFT_TOKEN` | [Get from Snap Store](https://snapcraft.io) | 1. Create account with jan.michael.kuehn.bln@gmail.com<br>2. Run locally: `snapcraft export-login --snaps folderzipper-versioning`<br>3. Copy the output |

### Optional Secrets (for advanced automation):

| Secret Name | Value | How to Get |
|-------------|-------|------------|
| `FLAT_MANAGER_TOKEN` | [Get from Flathub](https://flathub.org) | After first manual PR approval |

---

## 🚀 Platform Setup Instructions

### 1. **Winget** (Microsoft) - AUTOMATED ✅

**Status:** Ready to auto-submit on next release!

**What happens:**
- When you publish a GitHub release, workflow automatically:
  1. Downloads the .exe from releases
  2. Creates manifest using wingetcreate
  3. Submits PR to microsoft/winget-pkgs
  4. WinGet team reviews (2-3 days)
  5. Package available via `winget install FolderZipperVersioning`

**First Submission:** Manual PR will be created
**Updates:** Fully automated!

**Monitor:** Check "Pull requests" tab at https://github.com/microsoft/winget-pkgs

---

### 2. **Chocolatey** - AUTOMATED ✅

**Status:** Ready to auto-submit on next release!

**What happens:**
- When you publish a GitHub release, workflow automatically:
  1. Creates .nuspec manifest
  2. Creates chocolateyInstall.ps1
  3. Packs the package
  4. Pushes to Chocolatey Community Repository
  5. Moderation review (1-5 days)
  6. Package available via `choco install folderzipper-versioning`

**First Submission:** Requires moderation review
**Updates:** Automated after initial approval

**Monitor:** https://community.chocolatey.org/packages/folderzipper-versioning

**Account Setup:**
1. Go to https://community.chocolatey.org
2. Sign up with jan.michael.kuehn.bln@gmail.com
3. Password: Kjhategd7823--.ag
4. Get API Key from Account page
5. Add to GitHub Secrets as `CHOCOLATEY_API_KEY`

---

### 3. **Flathub** (Linux Flatpak) - SEMI-AUTOMATED ⚠️

**Status:** Build workflow ready, first submission manual

**What happens:**
- Workflow builds Flatpak package for testing
- **First submission:** Manual PR to https://github.com/flathub/flathub
- **After approval:** Can enable auto-deploy with token

**Steps for First Submission:**

1. **Test locally (optional):**
   ```bash
   flatpak-builder --user --install --force-clean build app-files/org.folderzipper.versioning.yml
   ```

2. **Fork Flathub repo:**
   - Go to https://github.com/flathub/flathub
   - Click "Fork"

3. **Create PR:**
   - Add your app as new folder in forked repo
   - Submit PR with description

4. **Review process:**
   - Flathub team reviews (3-10 days)
   - Respond to feedback
   - Once merged, your app is on Flathub!

**After Approval:**
- Add `FLAT_MANAGER_TOKEN` to GitHub Secrets
- Future releases auto-deploy

**Monitor:** https://github.com/flathub/flathub/pulls

---

### 4. **Snap Store** (Linux Snap) - AUTOMATED ✅

**Status:** Ready to auto-publish on next release!

**What happens:**
- When you publish a GitHub release, workflow automatically:
  1. Builds snap package using snapcraft.yaml
  2. Uploads to Snap Store
  3. Releases to stable channel
  4. Available via `sudo snap install folderzipper-versioning`

**Account Setup:**
1. Go to https://snapcraft.io
2. Sign up with jan.michael.kuehn.bln@gmail.com
3. Password: Kjhategd7823--.ag
4. Claim snap name: https://snapcraft.io/folderzipper-versioning
5. Generate token: `snapcraft export-login --snaps folderzipper-versioning`
6. Add to GitHub Secrets as `SNAPCRAFT_TOKEN`

**Monitor:** https://snapcraft.io/folderzipper-versioning

---

## 📋 Pre-Release Checklist

Before your next release, ensure:

- [ ] All workflows are in `.github/workflows/`
- [ ] `CHOCOLATEY_API_KEY` secret is set
- [ ] `SNAPCRAFT_TOKEN` secret is set
- [ ] Release tag format: `v1.0` (with 'v' prefix)
- [ ] Release includes `FolderZipperVersioning.exe` asset
- [ ] Release includes Linux executable (for Snap)

---

## 🎯 Next Release Process

1. **Update version in files:**
   - `snap/snapcraft.yaml` → version: '1.0.1'
   - `app-files/org.folderzipper.versioning.yml` → update version
   - `docs/CHANGELOG.md` → add new version

2. **Create GitHub Release:**
   - Tag: `v1.0.1`
   - Title: `FolderZipperVersioning v1.0.1`
   - Upload: `FolderZipperVersioning.exe`
   - Upload: Linux executable
   - Publish release

3. **Watch workflows:**
   - Go to https://github.com/codingismynewgaming/folder-zip-versioning/actions
   - All 4 workflows should trigger automatically
   - Check for errors

4. **Monitor approvals:**
   - Winget: Check microsoft/winget-pkgs PRs
   - Chocolatey: Check moderation status
   - Flathub: Manual PR needed (first time only)
   - Snap: Should be instant

---

## 🔧 Manual Commands (If Automation Fails)

### Winget (Manual)
```powershell
wingetcreate new "https://github.com/codingismynewgaming/folder-zip-versioning/releases/download/v1.0/FolderZipperVersioning.exe"
```

### Chocolatey (Manual)
```powershell
cd choco
choco pack folderzipper-versioning.nuspec
choco push folderzipper-versioning.*.nupkg --source https://push.chocolatey.org/
```

### Flatpak (Manual Test)
```bash
flatpak-builder --user --install --force-clean build app-files/org.folderzipper.versioning.yml
```

### Snap (Manual)
```bash
cd snap
snapcraft
snapcraft upload --release=stable folderzipper-versioning_1.0_amd64.snap
```

---

## 📧 Account Summary

All accounts use: **jan.michael.kuehn.bln@gmail.com**  
Password: **Kjhategd7823--.ag**

| Platform | URL | Status |
|----------|-----|--------|
| Chocolatey | https://community.chocolatey.org | ✅ Need API key |
| Snap Store | https://snapcraft.io | ✅ Need token |
| Flathub | https://flathub.org | Uses GitHub account |
| Winget | Uses GitHub account | ✅ No account needed |

---

## 🎉 Success Criteria

After next release, you should see:

- ✅ Winget: PR merged in microsoft/winget-pkgs
- ✅ Chocolatey: Package approved and listed
- ✅ Flathub: App listed on flathub.org (after manual PR)
- ✅ Snap: Package available in Snap Store

Users can then install via:
```bash
# Windows
winget install FolderZipperVersioning
choco install folderzipper-versioning

# Linux
flatpak install flathub org.folderzipper.versioning
sudo snap install folderzipper-versioning
```

---

**Questions?** Check workflow logs in GitHub Actions tab! 🚀
