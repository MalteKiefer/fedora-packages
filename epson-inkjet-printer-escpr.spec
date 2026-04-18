# Epson Inkjet Printer Driver (ESC/P-R) for Fedora (COPR)

Name:           epson-inkjet-printer-escpr
Version:        1.8.8
Release:        1%{?dist}
Summary:        Epson Inkjet Printer Driver (ESC/P-R) for Linux
License:        GPL-2.0-or-later
URL:            http://support.epson.net/linux/Printer/LSB_distribution_pages/en/escpr.php

Source0:        https://download-center.epson.com/f/module/e934c1f6-0fc1-43e5-8d3e-0de8f3a3d357/%{name}-%{version}-1.src.rpm

ExclusiveArch:  x86_64 aarch64

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  cups-devel

Requires:       cups
Requires:       ghostscript

%description
Epson Inkjet Printer Driver (ESC/P-R) for Linux. This package provides
CUPS filter and PPD files for a wide range of Epson inkjet printers,
enabling full printing support including color management, borderless
printing, and multiple paper sizes. The driver communicates with the
printer using the ESC/P-R raster command protocol.

%prep
# Source is a src.rpm containing a tarball
rpm2cpio %{SOURCE0} | cpio -idmv
tar xzf %{name}-%{version}-1.tar.gz
cd %{name}-%{version}
autoreconf -vif

%build
cd %{name}-%{version}

CFLAGS="%{optflags} -Wno-implicit-function-declaration"

%configure \
    --with-cupsfilterdir=%{_libdir}/cups/filter \
    --with-cupsppddir=%{_datadir}/ppd

%make_build

%install
cd %{name}-%{version}
%make_install

%files
%license %{name}-%{version}/COPYING
%{_libdir}/cups/filter/epson_escpr
%{_datadir}/ppd/Epson/
%{_libdir}/libescpr.*
