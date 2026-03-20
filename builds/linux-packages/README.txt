FolderZipperVersioning Linux Source Distribution v1.2

This archive contains everything needed to build Linux packages for
FolderZipperVersioning.

== Quick Build ==

Debian/Ubuntu:
  sudo apt-get install python3-tk dpkg-dev
  ./build-linux.sh --deb

Arch Linux:
  sudo pacman -S python-tkinter base-devel
  cd arch-linux && makepkg -si

Fedora/RHEL:
  sudo dnf install rpm python3-tkinter rpm-build
  ./build-linux.sh --rpm

== Manual Build ==

Debian Package:
  dpkg-deb --build debian builds/folder-zipper-versioning_1.2_all.deb

Arch Package:
  cd arch-linux
  makepkg --syncdeps --cleanbuild --noconfirm

RPM Package:
  rpmbuild -bb rpm/folder-zipper-versioning.spec --define "_topdir $PWD/rpmbuild"

== Installation ==

Debian/Ubuntu:
  sudo dpkg -i folder-zipper-versioning_1.2_all.deb
  sudo apt-get install -f  # Fix dependencies if needed

Arch Linux:
  sudo pacman -U folder-zipper-versioning-1.2-1.pkg.tar.zst

Fedora/RHEL:
  sudo dnf install folder-zipper-versioning-1.2.noarch.rpm

== Run Without Installing ==

  python3 app-files/zipper.py

== Requirements ==

- Python 3.8+
- Tkinter (python3-tk)

== License ==

MIT License - See LICENSE file
