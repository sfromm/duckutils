Name:		duckutils
Version:	0.1
Release:	1%{?dist}
Summary:    Collection of utility functions

BuildArch:  noarch
Group:		Development/Libraries
License:	GPLv3
URL:		https://github.com/sfromm/duckutils
Source0:	duckutils-%{version}.tar.gz

BuildRequires:	python-devel
Requires:	python
Requires:	PyYAML

%description
A collection of helper methods and functions for other python applications.

%prep
%setup -q


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{python_sitelib}/duckutils*
%doc README.md COPYING


%changelog
* Thu May 20 2013 Stephen Fromm <sfromm gmail com> - 0.1-0
- Initial version

