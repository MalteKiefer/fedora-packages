# Proton Authenticator for Fedora (COPR)
# Repackages the upstream .deb (Tauri-based app). No source build.

%global         debug_package %{nil}
%define         __strip /bin/true
%global         __provides_exclude_from ^/usr/lib/proton-authenticator/.*$
%global         __requires_exclude_from ^/usr/lib/proton-authenticator/.*$

Name:           proton-authenticator
Version:        1.1.4
Release:        4%{?dist}
Summary:        Proton Authenticator — 2FA app with secure sync and backup
License:        GPL-3.0-or-later
URL:            https://proton.me/authenticator

Source0:        https://proton.me/download/authenticator/linux/ProtonAuthenticator_%{version}_amd64.deb

ExclusiveArch:  x86_64

BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  coreutils
BuildRequires:  sed
BuildRequires:  desktop-file-utils

Requires:       cairo
Requires:       dbus-libs
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libsoup3
Requires:       pango
Requires:       webkit2gtk4.1

Provides:       proton-authenticator-bin = %{version}-%{release}
Conflicts:      proton-authenticator-bin

%description
Proton Authenticator is the free and open-source 2FA application from
Proton AG. Compatible with TOTP, URI imports and sync with Proton
accounts. This package repackages the upstream amd64 .deb build.

A workaround for WebKit on Wayland+NVIDIA and X11 is applied to the
installed .desktop entry (WEBKIT_DISABLE_DMABUF_RENDERER=1).

%prep
# The .deb is an ar archive; extract data.tar.* from it
cp -f %{SOURCE0} proton-authenticator.deb
ar x proton-authenticator.deb

# Tarball may be gzipped or zstd depending on upstream packaging
if   [ -f data.tar.gz  ]; then tar -xf data.tar.gz
elif [ -f data.tar.xz  ]; then tar -xf data.tar.xz
elif [ -f data.tar.zst ]; then tar --zstd -xf data.tar.zst
else
    echo "No recognized data.tar.* in .deb" >&2
    exit 1
fi

# Work around broken WebKit rendering on Wayland+NVIDIA and X11
sed -i 's|^Exec=proton-authenticator|Exec=env WEBKIT_DISABLE_DMABUF_RENDERER=1 proton-authenticator|' \
    "usr/share/applications/Proton Authenticator.desktop"

%build
# Prebuilt — nothing to compile.

%install
cp -a usr %{buildroot}/

# Normalize dir perms
find %{buildroot}/usr -type d -exec chmod 0755 {} +

# Ensure the bundled app binary is executable
if [ -f %{buildroot}%{_bindir}/%{name} ]; then
    chmod 0755 %{buildroot}%{_bindir}/%{name}
fi
# Application binary lives under /usr/lib/proton-authenticator/ on Tauri
if [ -f %{buildroot}%{_libdir}/%{name}/%{name} ]; then
    chmod 0755 %{buildroot}%{_libdir}/%{name}/%{name}
fi

# Rename the desktop file: RPM %%files cannot handle spaces in paths,
# and the space breaks desktop-database indexing on some tools.
mv "%{buildroot}%{_datadir}/applications/Proton Authenticator.desktop" \
   "%{buildroot}%{_datadir}/applications/%{name}.desktop"

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

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
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*

%changelog
* Sun Apr 19 2026 Malte Kiefer <malte.kiefer@aleph-alpha.com> - 1.1.4-3
- Initial Fedora COPR packaging, repack of upstream amd64 .deb
