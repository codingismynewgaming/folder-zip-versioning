"""Build script for FolderZipperVersioning - Windows and Linux"""
import subprocess
import os
import shutil
import sys
import platform

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, "app-files")
BUILD_DIR = os.path.join(BASE_DIR, "builds")

def get_system():
    """Get the current operating system."""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    return "unknown"

def build_windows():
    """Build Windows executable."""
    os.makedirs(BUILD_DIR, exist_ok=True)

    # Check if icon exists
    icon_path = os.path.join(APP_DIR, "app_icon.png")
    icon_arg = icon_path if os.path.exists(icon_path) else "NONE"

    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "FolderZipperVersioning",
        "--icon", icon_arg,
        "--add-data", "app-files;app-files",
        os.path.join(APP_DIR, "zipper.py")
    ]

    print("Building FolderZipperVersioning for Windows...")
    subprocess.run(cmd, check=True)

    # Move executable to builds folder (overwrite if exists)
    dist_exe = os.path.join(BASE_DIR, "dist", "FolderZipperVersioning.exe")
    target_exe = os.path.join(BUILD_DIR, "FolderZipperVersioning.exe")
    if os.path.exists(dist_exe):
        if os.path.exists(target_exe):
            os.remove(target_exe)
        shutil.move(dist_exe, BUILD_DIR)
        print(f"✓ Executable created: {target_exe}")

    # Cleanup
    for folder in ["build", "dist"]:
        path = os.path.join(BASE_DIR, folder)
        if os.path.exists(path):
            shutil.rmtree(path)

    print("✓ Windows build complete!")

def build_linux_executable():
    """Build Linux executable using PyInstaller."""
    os.makedirs(BUILD_DIR, exist_ok=True)

    # Check if icon exists
    icon_path = os.path.join(APP_DIR, "app_icon.png")
    icon_arg = icon_path if os.path.exists(icon_path) else None

    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "FolderZipperVersioning",
    ]
    
    if icon_arg:
        cmd.extend(["--icon", icon_arg])
    
    cmd.extend([
        "--add-data", "app-files:app-files",
        os.path.join(APP_DIR, "zipper.py")
    ])

    print("Building FolderZipperVersioning for Linux...")
    subprocess.run(cmd, check=True)

    # Move executable to builds folder (overwrite if exists)
    dist_exe = os.path.join(BASE_DIR, "dist", "FolderZipperVersioning")
    target_exe = os.path.join(BUILD_DIR, "FolderZipperVersioning")
    if os.path.exists(dist_exe):
        if os.path.exists(target_exe):
            os.remove(target_exe)
        shutil.move(dist_exe, BUILD_DIR)
        # Make executable
        os.chmod(target_exe, 0o755)
        print(f"✓ Executable created: {target_exe}")

    # Cleanup
    for folder in ["build", "dist"]:
        path = os.path.join(BASE_DIR, folder)
        if os.path.exists(path):
            shutil.rmtree(path)

    print("✓ Linux executable build complete!")

def build_deb_package():
    """Build Debian/Ubuntu package."""
    print("Building Debian package...")
    
    debian_dir = os.path.join(BASE_DIR, "debian")
    if not os.path.exists(debian_dir):
        print("Error: debian/ folder not found!")
        return False
    
    # Copy icon to debian folder for package build
    icon_src = os.path.join(APP_DIR, "icon.png")
    icon_dest = os.path.join(debian_dir, "icon.png")
    if os.path.exists(icon_src):
        shutil.copy(icon_src, icon_dest)
    
    # Build the package
    try:
        subprocess.run(["dpkg-buildpackage", "-us", "-uc", "-b"], 
                      cwd=BASE_DIR, check=True)
        
        # Move .deb file to builds folder
        for f in os.listdir(BASE_DIR):
            if f.endswith(".deb"):
                shutil.move(os.path.join(BASE_DIR, f), os.path.join(BUILD_DIR, f))
                print(f"Debian package created: {os.path.join(BUILD_DIR, f)}")
        
        # Cleanup copied icon
        if os.path.exists(icon_dest):
            os.remove(icon_dest)
        
        print("Debian package build complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building Debian package: {e}")
        return False
    except FileNotFoundError:
        print("Error: dpkg-buildpackage not found. Install dpkg-dev package.")
        return False

def build_arch_package():
    """Build Arch Linux package."""
    print("Building Arch Linux package...")
    
    arch_dir = os.path.join(BASE_DIR, "arch-linux")
    if not os.path.exists(arch_dir):
        print("Error: arch-linux/ folder not found!")
        return False
    
    # Copy required files to arch-linux folder
    for item in ["app-files", "LICENSE", "README.md"]:
        src = os.path.join(BASE_DIR, item)
        dest = os.path.join(arch_dir, item)
        if os.path.exists(src) and not os.path.exists(dest):
            if os.path.isdir(src):
                shutil.copytree(src, dest)
            else:
                shutil.copy(src, dest)
    
    try:
        subprocess.run(["makepkg", "--syncdeps", "--install", "--noconfirm"], 
                      cwd=arch_dir, check=True)
        
        # Move .pkg.tar.zst file to builds folder
        for f in os.listdir(arch_dir):
            if f.endswith(".pkg.tar.zst"):
                shutil.move(os.path.join(arch_dir, f), os.path.join(BUILD_DIR, f))
                print(f"Arch package created: {os.path.join(BUILD_DIR, f)}")
        
        print("Arch Linux package build complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building Arch package: {e}")
        return False
    except FileNotFoundError:
        print("Error: makepkg not found. Install archlinux-keyring and base-devel.")
        return False

def build_rpm_package():
    """Build RPM package for Fedora/RHEL."""
    print("Building RPM package...")
    
    rpm_dir = os.path.join(BASE_DIR, "rpm")
    if not os.path.exists(rpm_dir):
        print("Error: rpm/ folder not found!")
        return False
    
    # Create rpmbuild directory structure
    rpmbuild_base = os.path.join(BASE_DIR, "rpmbuild")
    for subdir in ["BUILD", "RPMS", "SOURCES", "SPECS", "SRPMS"]:
        os.makedirs(os.path.join(rpmbuild_base, subdir), exist_ok=True)
    
    # Copy spec file
    spec_src = os.path.join(rpm_dir, "folder-zipper-versioning.spec")
    spec_dest = os.path.join(rpmbuild_base, "SPECS", "folder-zipper-versioning.spec")
    shutil.copy(spec_src, spec_dest)
    
    # Create source tarball
    import tarfile
    source_name = f"folder-zipper-versioning-1.2"
    tarball_path = os.path.join(rpmbuild_base, "SOURCES", f"{source_name}.tar.gz")
    
    # Copy desktop file and icon to rpm folder
    shutil.copy(os.path.join(rpm_dir, "..", "debian", "folder-zipper-versioning.desktop"), 
                os.path.join(rpm_dir, "folder-zipper-versioning.desktop"))
    shutil.copy(os.path.join(APP_DIR, "icon.png"), os.path.join(rpm_dir, "icon.png"))
    
    with tarfile.open(tarball_path, "w:gz") as tar:
        tar.add(BASE_DIR, arcname=source_name, 
                filter=lambda x: None if x.name.endswith('.deb') or x.name.endswith('.pkg.tar.zst') or '.git' in x.name else x)
    
    try:
        subprocess.run(["rpmbuild", "-bb", "--define", f"_topdir {rpmbuild_base}", 
                       spec_dest], check=True)
        
        # Move .rpm file to builds folder
        rpm_build_dir = os.path.join(rpmbuild_base, "RPMS", "noarch")
        if os.path.exists(rpm_build_dir):
            for f in os.listdir(rpm_build_dir):
                if f.endswith(".rpm"):
                    shutil.move(os.path.join(rpm_build_dir, f), os.path.join(BUILD_DIR, f))
                    print(f"RPM package created: {os.path.join(BUILD_DIR, f)}")
        
        print("RPM package build complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building RPM package: {e}")
        return False
    except FileNotFoundError:
        print("Error: rpmbuild not found. Install rpm-build package.")
        return False

def build_all():
    """Build for all platforms."""
    system = get_system()
    print(f"Detected system: {system}")
    
    if system == "windows":
        build_windows()
    elif system == "linux":
        # Build executable first
        build_linux_executable()
        # Then try to build packages
        print("\n--- Building Linux Packages ---")
        build_deb_package()
        build_arch_package()
        build_rpm_package()
    elif system == "macos":
        print("macOS build not yet implemented")
    else:
        print("Unknown system, cannot build")

def build():
    """Main build function - builds for current platform."""
    system = get_system()
    
    if system == "windows":
        build_windows()
    elif system == "linux":
        build_linux_executable()
    elif system == "macos":
        print("macOS build not yet implemented")
    else:
        print("Unknown system, cannot build")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Build FolderZipperVersioning")
    parser.add_argument("--all", action="store_true", help="Build for all platforms (Linux only)")
    parser.add_argument("--deb", action="store_true", help="Build Debian package")
    parser.add_argument("--arch", action="store_true", help="Build Arch Linux package")
    parser.add_argument("--rpm", action="store_true", help="Build RPM package")
    parser.add_argument("--executable", action="store_true", help="Build executable only")
    
    args = parser.parse_args()
    
    if args.all:
        build_all()
    elif args.deb:
        build_deb_package()
    elif args.arch:
        build_arch_package()
    elif args.rpm:
        build_rpm_package()
    elif args.executable:
        build()
    else:
        build()
