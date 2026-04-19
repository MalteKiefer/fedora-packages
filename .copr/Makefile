.PHONY: srpm

SRCDIR = $(HOME)/rpmbuild/SOURCES
SPECBASE = $(notdir $(spec))

srpm:
	mkdir -p $(SRCDIR)
ifeq ($(SPECBASE),flutter.spec)
	spectool -g -R $(spec) 2>/dev/null || \
		curl -Lo $(SRCDIR)/flutter_linux_3.41.7-stable.tar.xz \
		"https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.41.7-stable.tar.xz"
endif
ifeq ($(SPECBASE),epson-inkjet-printer-escpr.spec)
	rm -f $(SRCDIR)/epson-inkjet-printer-escpr-*.src.rpm
	curl --user-agent Firefox -Lo $(SRCDIR)/epson-inkjet-printer-escpr-1.8.8-1.src.rpm \
		"https://download-center.epson.com/f/module/e934c1f6-0fc1-43e5-8d3e-0de8f3a3d357/epson-inkjet-printer-escpr-1.8.8-1.src.rpm"
endif
ifeq ($(SPECBASE),epson-inkjet-printer-escpr2.spec)
	rm -f $(SRCDIR)/epson-inkjet-printer-escpr2-*.tar.gz
	curl --user-agent Firefox -Lo $(SRCDIR)/epson-inkjet-printer-escpr2-1.2.38-1.tar.gz \
		"https://download-center.epson.com/f/module/42a6470c-53bf-4993-abad-ba5b4a1d5d84/epson-inkjet-printer-escpr2-1.2.38-1.tar.gz"
	cp $(dir $(spec))bug_x86_64.patch $(SRCDIR)/
	cp $(dir $(spec))enable_velvet_fine_art_paper.patch $(SRCDIR)/
endif
ifeq ($(SPECBASE),jdownloader2.spec)
	curl -Lo $(SRCDIR)/jdownloader2.tar.gz \
		"https://aur.archlinux.org/cgit/aur.git/snapshot/jdownloader2.tar.gz"
endif
	rpmbuild -bs --define "_sourcedir $(SRCDIR)" --define "_srcrpmdir $(outdir)" $(spec)
