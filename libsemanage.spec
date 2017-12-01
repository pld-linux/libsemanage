#
# Conditional build:
%bcond_without	python	# Python (any) bindings
%bcond_without	python2	# Python 2 binding
%bcond_without	python3	# Python 3 binding
#
%if %{without python}
%undefine	with_python2
%undefine	with_python3
%endif
Summary:	An interface for SELinux management
Summary(pl.UTF-8):	Interfejs do zarządzania SELinuksem
Name:		libsemanage
Version:	2.7
Release:	2
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/SELinuxProject/selinux/wiki/Releases
Source0:	https://raw.githubusercontent.com/wiki/SELinuxProject/selinux/files/releases/20170804/%{name}-%{version}.tar.gz
# Source0-md5:	a6b5c451fbe45ff9e3e0e65f2db0ae1d
Patch0:		%{name}-libexecdir.patch
URL:		https://github.com/SELinuxProject/selinux/wiki
BuildRequires:	bison
BuildRequires:	bzip2-devel
BuildRequires:	flex
BuildRequires:	libselinux-devel >= 2.7
BuildRequires:	libsepol-devel >= 2.7
%{?with_python2:BuildRequires:	python-devel >= 2}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	libselinux >= 2.7
Requires:	libsepol >= 2.7
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

%package -n python-semanage
Summary:	Python 2 binding for semanage library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki semanage
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-selinux >= 2.7

%description -n python-semanage
Python 2 binding for semanage library.

%description -n python-semanage -l pl.UTF-8
Wiązania Pythona 2 do biblioteki semanage.

%package -n python3-semanage
Summary:	Python 3 binding for semanage library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki semanage
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-selinux >= 2.7

%description -n python3-semanage
Python 3 binding for semanage library.

%description -n python3-semanage -l pl.UTF-8
Wiązania Pythona 3 do biblioteki semanage.

%prep
%setup -q
%patch0 -p1

%build
%{__make} -j1 all %{?with_python2:pywrap} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -fno-strict-aliasing" \
	LIBDIR=%{_libdir} \
	LIBEXECDIR=%{_libdir} \
	PYPREFIX=python2 \
	PYTHON=%{__python}

%if %{with python3}
%{__make} -j1 -C src pywrap \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -fno-strict-aliasing" \
	LIBDIR=%{_libdir} \
	LIBEXECDIR=%{_libdir} \
	PYPREFIX=python3 \
	PYTHON=%{__python3}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install %{?with_python2:install-pywrap} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	LIBEXECDIR=$RPM_BUILD_ROOT%{_libexecdir} \
	SHLIBDIR=$RPM_BUILD_ROOT/%{_lib} \
	PYPREFIX=python2 \
	PYSITEDIR=$RPM_BUILD_ROOT%{py_sitedir} \
	PYTHON=%{__python} \
	DESTDIR=$RPM_BUILD_ROOT

# changed in 2.4
install -d $RPM_BUILD_ROOT/%{_lib}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libsemanage.so.* $RPM_BUILD_ROOT/%{_lib}
# adjust .so symlink, make symlink across / absolute
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libsemanage.so.*) \
	$RPM_BUILD_ROOT%{_libdir}/libsemanage.so

%if %{with python2}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%if %{with python3}
%{__make} -C src install-pywrap \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	LIBEXECDIR=$RPM_BUILD_ROOT%{_libexecdir} \
	PYPREFIX=python3 \
	PYSITEDIR=$RPM_BUILD_ROOT%{py3_sitedir} \
	PYTHON=%{__python3} \
	DESTDIR=$RPM_BUILD_ROOT

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

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsemanage.so
%{_pkgconfigdir}/libsemanage.pc
%{_includedir}/semanage
%{_mandir}/man3/semanage_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libsemanage.a

%if %{with python2}
%files -n python-semanage
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_semanage.so
%{py_sitedir}/semanage.py[co]
%attr(755,root,root) %{_libexecdir}/selinux/semanage_migrate_store
%endif

%if %{with python3}
%files -n python3-semanage
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_semanage.cpython-*.so
%{py3_sitedir}/semanage.py
%{py3_sitedir}/__pycache__/semanage.cpython-*.py[co]
%endif
