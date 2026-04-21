.PHONY: srpm

SRCDIR   = $(HOME)/rpmbuild/SOURCES
SPECBASE = $(notdir $(spec))
SPECDIR  = $(dir $(spec))

srpm:
	mkdir -p $(SRCDIR)
	cp -f $(SPECDIR)*.patch $(SRCDIR)/ 2>/dev/null || :
	spectool -g -C $(SRCDIR) $(spec) || :
ifeq ($(SPECBASE),epson-inkjet-printer-escpr.spec)
	rm -f $(SRCDIR)/epson-inkjet-printer-escpr-*.src.rpm
	curl --user-agent Firefox -Lo $(SRCDIR)/epson-inkjet-printer-escpr-1.8.8-1.src.rpm \
		"https://download-center.epson.com/f/module/e934c1f6-0fc1-43e5-8d3e-0de8f3a3d357/epson-inkjet-printer-escpr-1.8.8-1.src.rpm"
endif
ifeq ($(SPECBASE),epson-inkjet-printer-escpr2.spec)
	rm -f $(SRCDIR)/epson-inkjet-printer-escpr2-*.tar.gz
	curl --user-agent Firefox -Lo $(SRCDIR)/epson-inkjet-printer-escpr2-1.2.38-1.tar.gz \
		"https://download-center.epson.com/f/module/42a6470c-53bf-4993-abad-ba5b4a1d5d84/epson-inkjet-printer-escpr2-1.2.38-1.tar.gz"
endif
	rpmbuild -bs --define "_sourcedir $(SRCDIR)" --define "_srcrpmdir $(outdir)" $(spec)
