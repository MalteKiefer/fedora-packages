# JDownloader 2 for Fedora (COPR)
# Ported from AUR PKGBUILD. Uses AUR snapshot for wrapper scripts,
# icons, desktop files, systemd unit. JDownloader self-updates at
# first run — fetches JDownloader.jar into /opt/JDownloader.

%global         debug_package %{nil}
%define         __strip /bin/true
%global         __provides_exclude_from ^/opt/JDownloader(Scripts)?/.*$
%global         __requires_exclude_from ^/opt/JDownloader(Scripts)?/.*$

Name:           jdownloader2
Version:        2.0
Release:        22%{?dist}
Summary:        Java-based download manager for one-click hosting sites
License:        GPL-3.0-or-later AND LicenseRef-JDownloader-Proprietary
URL:            https://jdownloader.org/

# AUR snapshot — contains wrapper scripts, icons, desktop/mime, service
Source0:        https://aur.archlinux.org/cgit/aur.git/snapshot/jdownloader2.tar.gz

BuildArch:      noarch

BuildRequires:  systemd-rpm-macros
BuildRequires:  coreutils

Requires:       hicolor-icon-theme
Requires:       java-17-openjdk-headless
Requires:       libarchive
Requires:       libXi
Requires:       libXtst
Requires:       dejavu-sans-fonts
Requires(post): shadow-utils

Suggests:       phantomjs

%description
JDownloader 2 is a Java-based download manager for one-click hosting
sites like Rapidshare, MEGA, and many others. This package ships the
wrapper scripts, desktop integration, icons, and a systemd unit for the
headless variant. JDownloader itself runs its own auto-updater on first
launch, fetching JDownloader.jar into /opt/JDownloader.

%prep
%setup -q -n jdownloader2

%build
# Nothing to compile — ships scripts only.

%install
# Wrapper scripts
install -d -m0755 %{buildroot}/opt/JDownloaderScripts
install -Dm0755 JDownloader                   %{buildroot}/opt/JDownloaderScripts/JDownloader
install -Dm0755 JDownloaderHeadless           %{buildroot}/opt/JDownloaderScripts/JDownloaderHeadless
install -Dm0755 JDownloaderHeadlessCtl        %{buildroot}/opt/JDownloaderScripts/JDownloaderHeadlessCtl
install -Dm0755 functions.sh                  %{buildroot}/opt/JDownloaderScripts/functions.sh
install -Dm0755 JDownloaderHeadlessCleanLogin %{buildroot}/opt/JDownloaderScripts/JDownloaderHeadlessCleanLogin

# MIME + desktop entries
install -Dm0644 jdownloader.xml       %{buildroot}%{_datadir}/mime/packages/jdownloader.xml
install -Dm0644 jdownloader.desktop   %{buildroot}%{_datadir}/applications/jdownloader.desktop
install -Dm0644 jd-containers.desktop %{buildroot}%{_datadir}/applications/jd-containers.desktop

# Mimetype icons
for s in 16 22 24 32 48 256; do
    install -Dm0644 "jd-container${s}.png" \
        "%{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/mimetypes/jd-container.png"
done

# App icons
for s in 16 22 24 32 48 256; do
    install -Dm0644 "jdownloader${s}.png" \
        "%{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/jdownloader.png"
done

# systemd unit
install -Dm0644 jdownloader.service %{buildroot}%{_unitdir}/jdownloader.service

# Install target dir for self-updating jar (setgid so group users can write)
install -d -m2775 %{buildroot}/opt/JDownloader

# CLI symlinks
install -d -m0755 %{buildroot}%{_bindir}
ln -sf /opt/JDownloaderScripts/JDownloader                   %{buildroot}%{_bindir}/JDownloader
ln -sf /opt/JDownloaderScripts/JDownloader                   %{buildroot}%{_bindir}/jdownloader
ln -sf /opt/JDownloaderScripts/JDownloaderHeadless           %{buildroot}%{_bindir}/JDownloaderHeadless
ln -sf /opt/JDownloaderScripts/JDownloaderHeadlessCtl        %{buildroot}%{_bindir}/JDownloaderHeadlessCtl
ln -sf /opt/JDownloaderScripts/JDownloaderHeadlessCleanLogin %{buildroot}%{_bindir}/JDownloaderHeadlessCleanLogin

%pre
# Group used for shared /opt/JDownloader access (setgid dir)
getent group jdownloader >/dev/null || groupadd -r jdownloader
exit 0

%post
%systemd_post jdownloader.service
# Refresh mime + icon caches
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{_datadir}/mime &>/dev/null || :

%preun
%systemd_preun jdownloader.service

%postun
%systemd_postun_with_restart jdownloader.service
if [ $1 -eq 0 ]; then
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    update-mime-database %{_datadir}/mime &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%dir /opt/JDownloaderScripts
/opt/JDownloaderScripts/JDownloader
/opt/JDownloaderScripts/JDownloaderHeadless
/opt/JDownloaderScripts/JDownloaderHeadlessCtl
/opt/JDownloaderScripts/functions.sh
/opt/JDownloaderScripts/JDownloaderHeadlessCleanLogin
%attr(2775,root,jdownloader) %dir /opt/JDownloader
%{_bindir}/JDownloader
%{_bindir}/jdownloader
%{_bindir}/JDownloaderHeadless
%{_bindir}/JDownloaderHeadlessCtl
%{_bindir}/JDownloaderHeadlessCleanLogin
%{_datadir}/applications/jdownloader.desktop
%{_datadir}/applications/jd-containers.desktop
%{_datadir}/mime/packages/jdownloader.xml
%{_datadir}/icons/hicolor/*/apps/jdownloader.png
%{_datadir}/icons/hicolor/*/mimetypes/jd-container.png
%{_unitdir}/jdownloader.service

%changelog
* Sat Apr 18 2026 Malte Kiefer <malte.kiefer@aleph-alpha.com> - 2.0-22
- Initial Fedora COPR packaging, ported from AUR jdownloader2 PKGBUILD
