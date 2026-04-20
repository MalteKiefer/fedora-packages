# Obsidian for Fedora (COPR)
# Repackages the upstream amd64 .deb. No source build.

%global         debug_package %{nil}
%define         __strip /bin/true
%global         __provides_exclude_from ^/opt/Obsidian/.*$
%global         __requires_exclude_from ^/opt/Obsidian/.*$

Name:           obsidian
Version:        1.12.7
Release:        1%{?dist}
Summary:        Knowledge base on top of a local folder of Markdown files
License:        LicenseRef-Obsidian-EULA
URL:            https://obsidian.md

Source0:        https://github.com/obsidianmd/obsidian-releases/releases/download/v%{version}/obsidian_%{version}_amd64.deb

ExclusiveArch:  x86_64

BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  coreutils
BuildRequires:  sed
BuildRequires:  desktop-file-utils

Requires:       gtk3
Requires:       libnotify
Requires:       nss
Requires:       libXScrnSaver
Requires:       libXtst
Requires:       xdg-utils
Requires:       at-spi2-core
Requires:       util-linux
Requires:       libsecret
Requires:       hicolor-icon-theme

Recommends:     libappindicator-gtk3

Provides:       obsidian-bin = %{version}-%{release}
Conflicts:      obsidian-bin

%description
Obsidian is a powerful knowledge base that works on top of a local
folder of plain text Markdown files. This package repackages the
upstream amd64 .deb with the bundled Electron runtime.

%prep
# .deb is an ar archive — extract data.tar.* from it
cp -f %{SOURCE0} obsidian.deb
ar x obsidian.deb

if   [ -f data.tar.xz  ]; then tar -xf data.tar.xz
elif [ -f data.tar.gz  ]; then tar -xf data.tar.gz
elif [ -f data.tar.zst ]; then tar --zstd -xf data.tar.zst
else
    echo "No recognized data.tar.* in .deb" >&2
    exit 1
fi

# Desktop file ships absolute path into /opt/Obsidian — rewrite to PATH binary
sed -i 's|/opt/Obsidian/obsidian|obsidian|' usr/share/applications/obsidian.desktop

%build
# Prebuilt — nothing to compile.

%install
install -d %{buildroot}/opt/Obsidian
cp -a opt/Obsidian/. %{buildroot}/opt/Obsidian/

# Normalize perms; ensure main binary and helpers executable
find %{buildroot}/opt/Obsidian -type d -exec chmod 0755 {} +
find %{buildroot}/opt/Obsidian -type f -exec chmod 0644 {} +
chmod 0755 %{buildroot}/opt/Obsidian/obsidian
[ -f %{buildroot}/opt/Obsidian/chrome_crashpad_handler ] && \
    chmod 0755 %{buildroot}/opt/Obsidian/chrome_crashpad_handler || :

# SUID on chrome-sandbox so Chromium sandbox works without --no-sandbox
[ -f %{buildroot}/opt/Obsidian/chrome-sandbox ] && \
    chmod 4755 %{buildroot}/opt/Obsidian/chrome-sandbox || :

# CLI symlink
install -d %{buildroot}%{_bindir}
ln -sf /opt/Obsidian/obsidian %{buildroot}%{_bindir}/obsidian

# Desktop entry (patched copy)
install -Dm0644 usr/share/applications/obsidian.desktop \
    %{buildroot}%{_datadir}/applications/obsidian.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/obsidian.desktop

# Icons from the .deb's /usr/share/icons tree
install -d %{buildroot}%{_datadir}/icons
cp -a usr/share/icons/hicolor %{buildroot}%{_datadir}/icons/

# Licenses
install -d %{buildroot}%{_licensedir}/%{name}
[ -f %{buildroot}/opt/Obsidian/LICENSE.electron.txt ] && \
    install -m0644 %{buildroot}/opt/Obsidian/LICENSE.electron.txt \
        %{buildroot}%{_licensedir}/%{name}/LICENSE.electron.txt || :
[ -f %{buildroot}/opt/Obsidian/LICENSES.chromium.html ] && \
    install -m0644 %{buildroot}/opt/Obsidian/LICENSES.chromium.html \
        %{buildroot}%{_licensedir}/%{name}/LICENSES.chromium.html || :

%post
update-desktop-database %{_datadir}/applications &>/dev/null || :
gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ]; then
    update-desktop-database %{_datadir}/applications &>/dev/null || :
    gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license %{_licensedir}/%{name}
%dir /opt/Obsidian
/opt/Obsidian
%{_bindir}/obsidian
%{_datadir}/applications/obsidian.desktop
%{_datadir}/icons/hicolor/*/apps/obsidian.png

%changelog
* Sun Apr 19 2026 Malte Kiefer <malte.kiefer@aleph-alpha.com> - 1.12.7-1
- Initial Fedora COPR packaging, repack of upstream amd64 .deb
