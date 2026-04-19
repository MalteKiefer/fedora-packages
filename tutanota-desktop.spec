# Tutanota / Tuta Mail Desktop for Fedora (COPR)
# Repackages the upstream signed AppImage. No source build.

%global         debug_package %{nil}
%define         __strip /bin/true
%global         __provides_exclude_from ^/opt/%{name}/.*$
%global         __requires_exclude_from ^/opt/%{name}/.*$

Name:           tutanota-desktop
Version:        340.260326.1
Release:        1%{?dist}
Summary:        Desktop client for Tuta Mail (formerly Tutanota) secure e-mail
License:        GPL-3.0-or-later
URL:            https://tuta.com/secure-email

Source0:        https://github.com/tutao/tutanota/releases/download/%{name}-release-%{version}/%{name}-linux.AppImage#/%{name}-%{version}.AppImage
Source1:        https://app.tuta.com/desktop/linux-sig.bin#/linux-sig-%{version}.bin
Source2:        https://github.com/tutao/tutanota/raw/%{name}-release-%{version}/tutao-pub.pem#/tutao-pub-%{version}.pem

ExclusiveArch:  x86_64

BuildRequires:  openssl
BuildRequires:  desktop-file-utils
BuildRequires:  coreutils
BuildRequires:  findutils

Requires:       alsa-lib
Requires:       gtk3
Requires:       libsecret
Requires:       nss
Requires:       libnotify
Requires:       libXScrnSaver
Requires:       libXtst
Requires:       at-spi2-core
Requires:       hicolor-icon-theme

Provides:       tutanota-desktop-bin = %{version}-%{release}
Conflicts:      tutanota-desktop-linux

%description
Tuta Mail Desktop (formerly Tutanota Desktop) is the official desktop
client for the secure end-to-end encrypted e-mail service by Tuta /
Tutanota GmbH. This package repackages the upstream, signed Linux
AppImage for Fedora. The AppImage signature is verified against the
upstream public key at build time.

%prep
# %%prep runs in %%{_builddir} — bring sources in and verify signature
cp -f %{SOURCE0} %{name}-%{version}.AppImage
cp -f %{SOURCE1} linux-sig-%{version}.bin
cp -f %{SOURCE2} tutao-pub-%{version}.pem

openssl dgst -sha512 \
    -verify tutao-pub-%{version}.pem \
    -signature linux-sig-%{version}.bin \
    %{name}-%{version}.AppImage

chmod +x %{name}-%{version}.AppImage
./%{name}-%{version}.AppImage --appimage-extract

# Rewrite bundled .desktop: AppImage's Exec points inside the mount,
# we need the installed path. Drop AppImage-only metadata.
desktop-file-edit \
    --set-key=Exec --set-value="/opt/%{name}/%{name} %U" \
    --remove-key=X-AppImage-Version \
    squashfs-root/%{name}.desktop

%build
# Prebuilt — nothing to compile.

%install
# Normalize dir perms inside the AppImage payload
find squashfs-root/{locales,resources,usr/share/icons} -type d -exec chmod 0755 {} + 2>/dev/null || :

install -d %{buildroot}/opt/%{name}
cp -a squashfs-root/. %{buildroot}/opt/%{name}/

# Required SUID bit so Chromium sandbox works without --no-sandbox
chmod 4755 %{buildroot}/opt/%{name}/chrome-sandbox

# Strip AppImage-only launcher/metadata that must not ship in an RPM
rm -f %{buildroot}/opt/%{name}/AppRun
rm -f %{buildroot}/opt/%{name}/%{name}.desktop
rm -f %{buildroot}/opt/%{name}/.DirIcon
rm -rf %{buildroot}/opt/%{name}/usr

# Sanity permissions on app resources
chmod 0644 %{buildroot}/opt/%{name}/resources/app.asar 2>/dev/null || :
chmod 0644 %{buildroot}/opt/%{name}/resources/app-update.yml 2>/dev/null || :

# CLI symlink
install -d %{buildroot}%{_bindir}
ln -sf /opt/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

# Desktop entry (patched copy)
install -Dm0644 squashfs-root/%{name}.desktop \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

# Icons from the AppImage's /usr/share/icons/hicolor tree
install -d %{buildroot}%{_datadir}/icons
cp -a squashfs-root/usr/share/icons/hicolor %{buildroot}%{_datadir}/icons/

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
%dir /opt/%{name}
/opt/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/mimetypes/*.png

%changelog
* Sun Apr 19 2026 Malte Kiefer <malte.kiefer@aleph-alpha.com> - 340.260326.1-1
- Initial Fedora COPR packaging, repack of upstream signed AppImage
