# Brother MFC-L3770CDW LPR/CUPS drivers for Fedora (COPR)
# Repackages upstream i386 .deb from Brother.

%global         debug_package %{nil}
%define         __strip /bin/true
%global         __provides_exclude_from ^/opt/brother/.*$
%global         __requires_exclude_from ^/opt/brother/.*$

Name:           brother-mfc-l3770cdw
Version:        1.0.2
Release:        1%{?dist}
Summary:        LPR and CUPS drivers for the Brother MFC-L3770CDW
License:        GPL-2.0-or-later AND Brother-EULA
URL:            https://support.brother.com/g/s/id/linux/en/index.html

Source0:        https://download.brother.com/welcome/dlf103935/mfcl3770cdwpdrv-1.0.2-0.i386.deb

ExclusiveArch:  x86_64

BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  coreutils
BuildRequires:  perl-interpreter

Requires:       cups
Requires:       glibc(x86-32)
Requires:       perl-interpreter

%description
Linux LPR and CUPS filter/PPD for the Brother MFC-L3770CDW color laser
multifunction printer. This package repackages the upstream i386 .deb
from Brother. The 32-bit print filter requires glibc(x86-32) at runtime.

The package installs the PPD to /usr/share/cups/model/Brother and a
CUPS filter symlink to /usr/lib64/cups/filter. It does not auto-add a
printer queue — run `lpadmin` or use the CUPS web UI after install.

%prep
cp -f %{SOURCE0} %{name}.deb
ar x %{name}.deb
tar -xf data.tar.gz

# Patch cupswrapper: Fedora has no /etc/init.d; neuter the init calls.
perl -i -pe 's#/etc/init\.d#/bin/true #g' \
    ./opt/brother/Printers/mfcl3770cdw/cupswrapper/cupswrappermfcl3770cdw

%build
# Prebuilt — nothing to compile.

%install
# Install /opt tree and /usr/bin/brprintconf_mfcl3770cdw
cp -a opt %{buildroot}/
cp -a usr %{buildroot}/

# Register PPD under the CUPS model tree
install -d %{buildroot}%{_datadir}/cups/model/Brother
install -m 0644 \
    opt/brother/Printers/mfcl3770cdw/cupswrapper/brother_mfcl3770cdw_printer_en.ppd \
    %{buildroot}%{_datadir}/cups/model/Brother/brother_mfcl3770cdw_printer_en.ppd

# CUPS filter symlink — points at the shipped lpd wrapper under /opt
install -d %{buildroot}%{_libdir}/cups/filter
ln -sf /opt/brother/Printers/mfcl3770cdw/cupswrapper/brother_lpdwrapper_mfcl3770cdw \
    %{buildroot}%{_libdir}/cups/filter/brother_lpdwrapper_mfcl3770cdw

# Normalize perms
find %{buildroot}/opt/brother -type d -exec chmod 0755 {} +
chmod 0755 %{buildroot}%{_bindir}/brprintconf_mfcl3770cdw
chmod 0755 %{buildroot}/opt/brother/Printers/mfcl3770cdw/lpd/brmfcl3770cdwfilter
chmod 0755 %{buildroot}/opt/brother/Printers/mfcl3770cdw/lpd/filter_mfcl3770cdw
chmod 0755 %{buildroot}/opt/brother/Printers/mfcl3770cdw/cupswrapper/brother_lpdwrapper_mfcl3770cdw
chmod 0755 %{buildroot}/opt/brother/Printers/mfcl3770cdw/cupswrapper/cupswrappermfcl3770cdw

%post
if [ $1 -eq 1 ] && command -v systemctl >/dev/null 2>&1; then
    systemctl reload-or-try-restart cups.service &>/dev/null || :
fi

%postun
if [ $1 -eq 0 ] && command -v systemctl >/dev/null 2>&1; then
    systemctl reload-or-try-restart cups.service &>/dev/null || :
fi

%files
%{_bindir}/brprintconf_mfcl3770cdw
%{_datadir}/cups/model/Brother/brother_mfcl3770cdw_printer_en.ppd
%{_libdir}/cups/filter/brother_lpdwrapper_mfcl3770cdw
/opt/brother/Printers/mfcl3770cdw/

%changelog
* Tue Apr 21 2026 Malte Kiefer <malte.kiefer@aleph-alpha.com> - 1.0.2-1
- Initial Fedora COPR packaging, repack of upstream Brother i386 .deb
