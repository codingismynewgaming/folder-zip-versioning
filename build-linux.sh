#!/bin/bash
# Build Linux packages for FolderZipperVersioning v1.2

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔨 Building Linux packages for FolderZipperVersioning v1.2..."

# Create builds directory
mkdir -p builds

# Build .deb package
echo "📦 Building Debian package..."
dpkg-deb --build debian builds/folder-zipper-versioning_1.2_all.deb
echo "✓ Debian package created: builds/folder-zipper-versioning_1.2_all.deb"

# Build Arch package (requires makepkg)
if command -v makepkg &> /dev/null; then
    echo "📦 Building Arch Linux package..."
    cd arch-linux
    makepkg --syncdeps --cleanbuild --noconfirm
    mv folder-zipper-versioning-*.pkg.tar.zst ../builds/
    cd ..
    echo "✓ Arch package created"
else
    echo "⚠ makepkg not found, skipping Arch build"
fi

# Build RPM package (requires rpmbuild)
if command -v rpmbuild &> /dev/null; then
    echo "📦 Building RPM package..."
    rpmbuild -bb rpm/folder-zipper-versioning.spec --define "_topdir $SCRIPT_DIR/rpmbuild"
    mv rpmbuild/RPMS/noarch/*.rpm builds/
    echo "✓ RPM package created"
else
    echo "⚠ rpmbuild not found, skipping RPM build"
fi

echo ""
echo "✅ All Linux packages built successfully!"
echo "📁 Packages location: builds/"
ls -lh builds/
