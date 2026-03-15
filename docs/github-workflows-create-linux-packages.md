# How to Properly Create Linux Packages using GitHub Actions

When building Linux packages (Debian `.deb`, Arch Linux `.pkg.tar.zst`, and Red Hat `.rpm`) in CI/CD pipelines, using third-party GitHub Actions can often lead to path mismatches, missing dependencies, and environment issues. 

The most robust and reliable approach is to use **native build tools inside OS-specific Docker containers**. This ensures the build environment exactly matches the target distribution.

## Key Principles for Reliable Linux Builds

1.  **Use Native Tools:** Use `dpkg-deb` for Debian, `rpmbuild` for RPM, and `makepkg` for Arch Linux. Avoid wrappers if possible.
2.  **Use OS-Specific Containers:** Run the build steps inside containers that match the target OS (e.g., `ubuntu:latest` for Debian, `fedora:latest` for RPM, `archlinux:latest` for Arch).
3.  **Handle Artifacts Properly:** Distinguish between manual runs (`workflow_dispatch`) and actual releases (`release`). Use `actions/upload-artifact` for testing manual builds and `upload-release-action` for publishing releases.

---

## 1. Building Debian Packages (`.deb`)

Debian packages can usually be built directly on the default `ubuntu-latest` GitHub runner without needing a separate container, as Ubuntu is Debian-based and has the necessary tools pre-installed.

### Strategy
- Create the exact directory structure required by Debian (`usr/bin`, `usr/share/applications`, `DEBIAN`, etc.).
- Copy your application files into this mock root directory.
- Create the `control` file inside the `DEBIAN` directory.
- Use `dpkg-deb --build <directory>` to package it.

### Example Snippet
```yaml
build-deb:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Build Debian package
      run: |
        # 1. Create structure
        mkdir -p debian-pkg/usr/bin
        mkdir -p debian-pkg/DEBIAN
        
        # 2. Copy files
        cp my_app debian-pkg/usr/bin/
        
        # 3. Create control file
        cat > debian-pkg/DEBIAN/control << 'EOF'
        Package: my-app
        Version: 1.0
        Architecture: all
        Depends: python3
        Maintainer: Your Name
        Description: My awesome app
        EOF
        
        # 4. Build package
        mkdir -p builds
        dpkg-deb --build debian-pkg builds/my-app_1.0_all.deb
```

---

## 2. Building RPM Packages (`.rpm`)

RPM builds require `rpm-build` and often specific development packages. Running this on an Ubuntu runner directly is prone to errors. It is highly recommended to use a **Fedora container**.

### Strategy
- Use `container: image: fedora:latest` in your job.
- Install `rpm-build` and necessary dependencies (like `python3-devel`) using `dnf`.
- Set up the standard `rpmbuild` directory tree (`~/rpmbuild/{SOURCES,SPECS,BUILD,RPMS,SRPMS}`).
- Create a source tarball and place it in `SOURCES`.
- Run `rpmbuild -ba <spec_file>`.

### Example Snippet
```yaml
build-rpm:
  runs-on: ubuntu-latest
  container:
    image: fedora:latest
  steps:
    - name: Install build tools
      run: dnf install -y rpm-build python3-devel
      
    - uses: actions/checkout@v4
    - name: Build RPM package
      run: |
        # 1. Setup rpmbuild tree
        mkdir -p ~/rpmbuild/{SOURCES,SPECS,BUILD,RPMS,SRPMS}
        
        # 2. Prepare sources
        mkdir -p my-app-1.0
        cp -r src my-app-1.0/
        tar -czf ~/rpmbuild/SOURCES/my-app-1.0.tar.gz my-app-1.0
        cp my-app.spec ~/rpmbuild/SPECS/
        
        # 3. Build package
        rpmbuild -ba ~/rpmbuild/SPECS/my-app.spec
        
        # 4. Collect output
        mkdir -p builds
        cp ~/rpmbuild/RPMS/noarch/*.rpm builds/
```

---

## 3. Building Arch Linux Packages (`.pkg.tar.zst`)

Arch Linux builds use `makepkg`, which strictly refuses to run as the `root` user. Since GitHub Actions containers default to `root`, you must create a standard user specifically for the build step.

### Strategy
- Use `container: image: archlinux:latest` in your job.
- Install `base-devel`, `git`, and `sudo` using `pacman`.
- Create a non-root user (e.g., `builder`) and give it passwordless sudo access.
- Prepare the source files (like the source tarball) in the directory containing your `PKGBUILD`.
- Change ownership of the build directory to the `builder` user.
- Execute `makepkg` as the `builder` user.

### Example Snippet
```yaml
build-arch:
  runs-on: ubuntu-latest
  container:
    image: archlinux:latest
  steps:
    - name: Install build tools
      run: pacman -Syu --noconfirm base-devel git sudo
      
    - uses: actions/checkout@v4
    - name: Build Arch package
      run: |
        # 1. Create non-root user
        useradd -m builder
        echo "builder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
        chown -R builder .
        
        # 2. Prepare sources for PKGBUILD
        tar -czf arch-linux/my-app-1.0.tar.gz src/
        
        # 3. Build package as non-root
        cd arch-linux
        sudo -u builder makepkg --noconfirm -s
        
        # 4. Collect output
        cd ..
        mkdir -p builds
        cp arch-linux/*.pkg.tar.zst builds/
```

---

## Handling Workflow Artifacts vs. Releases

A common mistake is trying to upload files to a GitHub Release during a manual workflow run (`workflow_dispatch`). If no release tag exists, the action will fail.

Always split your outputs:
1.  **Artifacts:** Always upload the built packages as artifacts so you can download them from the Actions tab.
2.  **Releases:** Only attempt to attach the files to a release if the workflow was triggered by a release event.

### Example Snippet
```yaml
      # Always available for download on the GitHub Actions page
      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: linux-packages
          path: builds/*

      # Only executes when a GitHub Release is published
      - name: Upload to Release
        if: github.event_name == 'release'
        uses: svenstaro/upload-release-action@v2
        with:
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          file: builds/*
          tag: ${{ github.ref }}
          overwrite: true
```
