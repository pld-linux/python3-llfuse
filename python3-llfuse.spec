#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define		module	llfuse
Summary:	Python bindings for the low level FUSE API
Name:		python3-%{module}
Version:	1.5.1
Release:	1
License:	GPL v2
Group:		Libraries/Python
Source0:	https://pypi.debian.net/llfuse/%{module}-%{version}.tar.gz
# Source0-md5:	8562120ca5cf3efeaac6607b05230037
Patch0:		x32.patch
URL:		https://github.com/python-llfuse/python-llfuse
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	libfuse-devel >= 2.8.0
BuildRequires:	rpm-pythonprov
BuildRequires:	python-Cython
BuildRequires:	python3-devel
BuildRequires:	python3-contextlib2
BuildRequires:	python3-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python bindings for the low level FUSE API.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}
%ifarch x32
%patch -P0 -p1
%endif

%build
./setup.py build_cython

%py3_build

%if %{with tests}
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$(echo $PWD/build-3/lib*)" test
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
      $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}/*.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes.rst
%attr(755,root,root) %{py3_sitedir}/%{module}.*.so
%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
