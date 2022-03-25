#
# Conditional build:
%bcond_without	python	# Python 3 bindings
#
Summary:	An interface for SELinux management
Summary(pl.UTF-8):	Interfejs do zarządzania SELinuksem
Name:		libsemanage
Version:	3.1
Release:	2
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/SELinuxProject/selinux/wiki/Releases
Source0:	https://github.com/SELinuxProject/selinux/releases/download/20200710/%{name}-%{version}.tar.gz
# Source0-md5:	d16eee8c1dc8cf43f59957d575d6bd29
Patch0:		%{name}-libexecdir.patch
URL:		https://github.com/SELinuxProject/selinux/wiki
BuildRequires:	audit-libs-devel
BuildRequires:	bison
BuildRequires:	bzip2-devel
BuildRequires:	flex
BuildRequires:	libselinux-devel >= 3.1
BuildRequires:	libsepol-devel >= 3.1
%{?with_python:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	libselinux >= 3.1
Requires:	libsepol >= 3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An interface for SELinux management.

%description -l pl.UTF-8
Interfejs do zarządzania SELinuksem.

%package devel
Summary:	Header files for libsemanage library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libsemanage
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for libsemanage library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki libsemanage.

%package static
Summary:	Static version of libsemanage library
Summary(pl.UTF-8):	Statyczna wersja biblioteki libsemanage
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of libsemanage library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki libsemanage.

%package -n python3-semanage
Summary:	Python 3 binding for semanage library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki semanage
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-selinux >= 3.1

%description -n python3-semanage
Python 3 binding for semanage library.

%description -n python3-semanage -l pl.UTF-8
Wiązania Pythona 3 do biblioteki semanage.

%prep
%setup -q
%patch0 -p1

%build
%{__make} -j1 all %{?with_python:pywrap} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -fno-strict-aliasing" \
	LIBDIR=%{_libdir} \
	LIBEXECDIR=%{_libexecdir} \
	PYPREFIX=python3 \
	PYTHON=%{__python3}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install %{?with_python:install-pywrap} \
	LIBDIR=%{_libdir} \
	LIBEXECDIR=%{_libexecdir} \
	PYPREFIX=python3 \
	PYSITEDIR=%{py_sitedir} \
	PYTHON=%{__python3} \
	DESTDIR=$RPM_BUILD_ROOT

# changed in 2.4
install -d $RPM_BUILD_ROOT/%{_lib}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libsemanage.so.* $RPM_BUILD_ROOT/%{_lib}
# adjust .so symlink, make symlink across / absolute
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libsemanage.so.*) \
	$RPM_BUILD_ROOT%{_libdir}/libsemanage.so

%if %{with python}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libsemanage.so.1
%dir %{_sysconfdir}/selinux
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/selinux/semanage.conf
%dir %{_libexecdir}/selinux
%{_mandir}/man5/semanage.conf.5*
%lang(ru) %{_mandir}/ru/man5/semanage.conf.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsemanage.so
%{_pkgconfigdir}/libsemanage.pc
%{_includedir}/semanage
%{_mandir}/man3/semanage_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libsemanage.a

%if %{with python}
%files -n python3-semanage
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_semanage.cpython-*.so
%{py3_sitedir}/semanage.py
%{py3_sitedir}/__pycache__/semanage.cpython-*.py[co]
%attr(755,root,root) %{_libexecdir}/selinux/semanage_migrate_store
%endif
