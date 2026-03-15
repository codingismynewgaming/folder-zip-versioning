Name:           folder-zipper-versioning
Version:        1.0
Release:        1%{?dist}
Summary:        Folder Zipper with automatic versioning
License:        MIT
URL:            https://github.com/codingismynewgaming/folder-zip-versioning
BuildArch:      noarch

# Dependencies
Requires:       python3
Requires:       python3-tkinter

# Source files
Source0:        %{name}-%{version}.tar.gz
Source1:        folder-zipper-versioning.desktop
Source2:        icon.png

# Build requirements
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
A Python Tkinter GUI application that zips folders with automatic version numbering.

Features:
- Easy folder selection via GUI
- Auto version numbering (001, 002, 003...)
- Custom version input
- Timestamp in filenames
- Dark mode support
- Directory navigation

%prep
%setup -q

%install
# Create installation directories
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps
mkdir -p %{buildroot}/usr/share/licenses/%{name}
mkdir -p %{buildroot}/usr/share/doc/%{name}

# Install the main application
install -Dm 755 app-files/zipper.py %{buildroot}/usr/bin/folder-zipper-versioning

# Install desktop file
install -Dm 644 %{SOURCE1} %{buildroot}/usr/share/applications/folder-zipper-versioning.desktop

# Install icon
install -Dm 644 %{SOURCE2} %{buildroot}/usr/share/icons/hicolor/256x256/apps/folder-zipper-versioning.png

# Install license and documentation
install -Dm 644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
install -Dm 644 README.md %{buildroot}/usr/share/doc/%{name}/README.md

%post
# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database -q /usr/share/applications 2>/dev/null || :
fi

# Update icon cache
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || :
fi

%postun
# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database -q /usr/share/applications 2>/dev/null || :
fi

# Update icon cache
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -q -f /usr/share/icons/hicolor 2>/dev/null || :
fi

%files
/usr/bin/folder-zipper-versioning
/usr/share/applications/folder-zipper-versioning.desktop
/usr/share/icons/hicolor/256x256/apps/folder-zipper-versioning.png
/usr/share/licenses/%{name}/LICENSE
/usr/share/doc/%{name}/README.md

%changelog
* Sat Mar 14 2026 Your Name <your.email@example.com> - 1.0-1
- Initial package release
- Folder Zipper with versioning GUI application
