# Flutter SDK RPM Spec for Fedora (COPR)
# Flutter ships a pre-built SDK bundle including Dart – we repackage it.

%global         flutter_version 3.41.7
%global         dart_version    3.11.5
%global         install_dir     %{_libdir}/flutter

Name:           flutter
Version:        %{flutter_version}
Release:        5%{?dist}
Summary:        Google's UI toolkit for building natively compiled applications
License:        BSD-3-Clause
URL:            https://flutter.dev

Source0:        https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_%{flutter_version}-stable.tar.xz

# Flutter is only available for x86_64 and aarch64
ExclusiveArch:  x86_64 aarch64

# Runtime dependencies for Flutter desktop / toolchain
Requires:       bash
Requires:       curl
Requires:       git
Requires:       unzip
Requires:       which
Requires:       xz
# GTK / desktop embedding (flutter linux-desktop)
Requires:       gtk3-devel
Requires:       clang
Requires:       cmake
Requires:       ninja-build
Requires:       pkg-config
Requires:       libstdc++-devel

# Build dependencies (we only unpack, but rpmbuild still needs these)
BuildRequires:  tar
BuildRequires:  xz

# The SDK ships pre-built binaries – nothing to compile
%global         debug_package %{nil}

# Do not strip pre-built binaries
%define         __strip /bin/true

# Do not generate auto-provides / auto-requires from bundled libs
%global         __provides_exclude_from %{install_dir}/.*
%global         __requires_exclude_from %{install_dir}/.*

%description
Flutter is Google's portable UI toolkit for building beautiful, natively
compiled applications for mobile, web, and desktop from a single codebase.

This package installs the Flutter SDK (including Dart %{dart_version}) to
%{install_dir} and places wrapper scripts in /usr/bin.

%prep
%setup -q -n flutter

%build
# Pre-built SDK – nothing to build.
# Run precache so all artifacts are present in the package.
export PUB_CACHE="%{_builddir}/.pub-cache"
bin/flutter precache --linux 2>/dev/null || true

%install
# Install the SDK tree
install -d %{buildroot}%{install_dir}
cp -a . %{buildroot}%{install_dir}/

# Drop CI metadata + transient caches. Keep .git: flutter tool refuses to
# run without it (bin/internal/shared.sh checks $FLUTTER_ROOT/.git).
# Wrapper scripts inject safe.directory to silence dubious-ownership.
rm -rf %{buildroot}%{install_dir}/.github \
       %{buildroot}%{install_dir}/.ci \
       %{buildroot}%{install_dir}/.pub-cache

# Flutter writes engine.stamp + downloads artifacts into bin/cache on every
# invocation, and runs `git fetch --tags` against $FLUTTER_ROOT/.git to
# resolve versions. Add world-writable bit (preserve exec on binaries like
# dart) and a sticky bit on dirs so users can't clobber each other's files.
chmod -R a+w %{buildroot}%{install_dir}/bin/cache \
             %{buildroot}%{install_dir}/.git
find %{buildroot}%{install_dir}/bin/cache \
     %{buildroot}%{install_dir}/.git \
     -type d -exec chmod +t {} +

# Create wrapper scripts
install -d %{buildroot}%{_bindir}

cat > %{buildroot}%{_bindir}/flutter << 'WRAPPER'
#!/usr/bin/env bash
export FLUTTER_ROOT="%{install_dir}"
# Trust the system-wide SDK checkout regardless of invoking user.
export GIT_CONFIG_COUNT=1
export GIT_CONFIG_KEY_0=safe.directory
export GIT_CONFIG_VALUE_0="${FLUTTER_ROOT}"
exec "${FLUTTER_ROOT}/bin/flutter" "$@"
WRAPPER
chmod 0755 %{buildroot}%{_bindir}/flutter

cat > %{buildroot}%{_bindir}/dart << 'WRAPPER'
#!/usr/bin/env bash
export FLUTTER_ROOT="%{install_dir}"
export GIT_CONFIG_COUNT=1
export GIT_CONFIG_KEY_0=safe.directory
export GIT_CONFIG_VALUE_0="${FLUTTER_ROOT}"
exec "${FLUTTER_ROOT}/bin/dart" "$@"
WRAPPER
chmod 0755 %{buildroot}%{_bindir}/dart

# Profile script for FLUTTER_ROOT / PUB_CACHE
install -d %{buildroot}%{_sysconfdir}/profile.d

cat > %{buildroot}%{_sysconfdir}/profile.d/flutter.sh << 'PROFILE'
export FLUTTER_ROOT="%{install_dir}"
export PUB_CACHE="${HOME}/.pub-cache"
PROFILE
chmod 0644 %{buildroot}%{_sysconfdir}/profile.d/flutter.sh

%files
%license LICENSE
%doc README.md CONTRIBUTING.md
%{install_dir}
%{_bindir}/flutter
%{_bindir}/dart
%{_sysconfdir}/profile.d/flutter.sh
