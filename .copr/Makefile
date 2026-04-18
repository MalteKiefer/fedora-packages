.PHONY: srpm

srpm:
	dnf install -y rpm-build curl cpio
	# --- Flutter ---
	spectool -g -R ../flutter.spec 2>/dev/null || \
		curl -Lo $(HOME)/rpmbuild/SOURCES/flutter_linux_3.41.7-stable.tar.xz \
		"https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.41.7-stable.tar.xz"
	rpmbuild -bs --define "_sourcedir $(HOME)/rpmbuild/SOURCES" --define "_srcrpmdir $(outdir)" ../flutter.spec
	# --- ESCPR ---
	curl --user-agent Firefox -Lo $(HOME)/rpmbuild/SOURCES/epson-inkjet-printer-escpr-1.8.8-1.src.rpm \
		"https://download-center.epson.com/f/module/e934c1f6-0fc1-43e5-8d3e-0de8f3a3d357/epson-inkjet-printer-escpr-1.8.8-1.src.rpm"
	rpmbuild -bs --define "_sourcedir $(HOME)/rpmbuild/SOURCES" --define "_srcrpmdir $(outdir)" ../epson-inkjet-printer-escpr.spec
	# --- ESCPR2 ---
	curl --user-agent Firefox -Lo $(HOME)/rpmbuild/SOURCES/epson-inkjet-printer-escpr2-1.2.38-1.tar.gz \
		"https://download-center.epson.com/f/module/42a6470c-53bf-4993-abad-ba5b4a1d5d84/epson-inkjet-printer-escpr2-1.2.38-1.tar.gz"
	cp ../bug_x86_64.patch $(HOME)/rpmbuild/SOURCES/
	cp ../enable_velvet_fine_art_paper.patch $(HOME)/rpmbuild/SOURCES/
	rpmbuild -bs --define "_sourcedir $(HOME)/rpmbuild/SOURCES" --define "_srcrpmdir $(outdir)" ../epson-inkjet-printer-escpr2.spec
