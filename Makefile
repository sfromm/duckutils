NAME=duckutils
VERSION := $(shell grep __version duckutils/__init__.py | sed -e 's|^.*= ||' -e "s|'||g" )

# Get the branch information from git
ifneq ($(shell which git),)
GIT_DATE := $(shell git log -n 1 --format="%ai")
endif

ifeq ($(OS), FreeBSD)
DATE := $(shell date -j -f "%Y-%m-%d %H:%M:%s"  "$(GIT_DATE)" +%Y%m%d%H%M)
else
ifeq ($(OS), Darwin)
DATE := $(shell date -j -f "%Y-%m-%d %H:%M:%S"  "$(GIT_DATE)" +%Y%m%d%H%M)
else
DATE := $(shell date --utc --date="$(GIT_DATE)" +%Y%m%d%H%M)
endif
endif

# RPM build parameters
RPMSPECDIR = packaging/rpm
RPMSPEC = $(RPMSPECDIR)/duckutils.spec
RPMDIST = $(shell rpm --eval '%dist')
RPMRELEASE = 1
ifeq ($(OFFICIAL),)
RPMRELEASE = 0.git$(DATE)
endif
RPMNVR = "$(NAME)-$(VERSION)-$(RPMRELEASE)$(RPMDIST)"


all: clean python

test:
	DUCKUTILS_SMTP_RECIPIENT=stephenf@nero.net DUCKUTILS_SMTP_SERVER=mail.nero.net PYTHONPATH=duckutils nosetests -d -v 

clean:
	@echo 'Cleaning up'
	rm -rf build
	rm -rf dist
	find . -type f -regex ".*\.py[co]$$" -delete

python:
	python setup.py build

install:
	python setup.py install

pep8:
	@echo 'Running PEP8 compliance tests'
	-pep8 -r --ignore=E302 duckutils

sdist:
	python setup.py sdist -t MANIFEST.in

rpmcommon: sdist
	@mkdir -p rpm-build
	@cp dist/*gz rpm-build/
	@echo '$(VERSION)'
	@sed -e 's/^Version:.*/Version: $(VERSION)/' \
		-e 's/^Release:.*/Release: $(RPMRELEASE)%{?dist}/' \
		$(RPMSPEC) > rpm-build/$(NAME).spec

srpm: rpmcommon
	@rpmbuild --define "_topdir %(pwd)/rpm-build" \
		--define "_builddir %{_topdir}" \
		--define "_rpmdir %{_topdir}" \
		--define "_srcrpmdir %{_topdir}" \
		--define "_specdir $(RPMSPECDIR)" \
		--define "_sourcedir %{_topdir}" \
		-bs rpm-build/$(NAME).spec
	@rm -f rpm-build/$(NAME).spec
	@echo "SRPM is built:"
	@echo "    rpm-build/$(RPMNVR).src.rpm"

rpm: rpmcommon
	@rpmbuild --define "_topdir %(pwd)/rpm-build" \
		--define "_builddir %{_topdir}" \
		--define "_rpmdir %{_topdir}" \
		--define "_srcrpmdir %{_topdir}" \
		--define "_specdir $(RPMSPECDIR)" \
		--define "_sourcedir %{_topdir}" \
		-ba rpm-build/$(NAME).spec
	@rm -f rpm-build/$(NAME).spec
	@echo "RPM is built:"
	@echo "    rpm-build/$(RPMNVR).noarch.rpm"

