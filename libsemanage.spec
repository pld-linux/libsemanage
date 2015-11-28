Summary:	An interface for SELinux management
Summary(pl.UTF-8):	Interfejs do zarządzania SELinuksem
Name:		libsemanage
Version:	2.4
Release:	2
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/SELinuxProject/selinux/wiki/Releases
Source0:	https://raw.githubusercontent.com/wiki/SELinuxProject/selinux/files/releases/20150202/%{name}-%{version}.tar.gz
# Source0-md5:	cd551eb1cc5d20652660bda037972f0d
Patch0:		%{name}-libexecdir.patch
URL:		https://github.com/SELinuxProject/selinux/wiki
BuildRequires:	bison
BuildRequires:	bzip2-devel
BuildRequires:	flex
BuildRequires:	libselinux-devel >= 2.4
BuildRequires:	libsepol-devel >= 2.4
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	ustr-devel
Requires:	libselinux >= 2.4
Requires:	libsepol >= 2.4
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
Summary:	Python binding for semanage library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki semanage
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-selinux >= 2.4
%pyrequires_eq	python-libs

%description -n python-semanage
Python binding for semanage library.

%description -n python-semanage -l pl.UTF-8
Wiązania Pythona do biblioteki semanage.

%prep
%setup -q
%patch0 -p1

%build
%{__make} -j1 all pywrap \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -fno-strict-aliasing" \
	LIBEXECDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install install-pywrap \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	LIBEXECDIR=$RPM_BUILD_ROOT%{_libdir} \
	SHLIBDIR=$RPM_BUILD_ROOT/%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT

# changed in 2.4
install -d $RPM_BUILD_ROOT/%{_lib}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libsemanage.so.* $RPM_BUILD_ROOT/%{_lib}
# adjust .so symlink, make symlink across / absolute
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libsemanage.so.*) \
	$RPM_BUILD_ROOT%{_libdir}/libsemanage.so

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) /%{_lib}/libsemanage.so.*
%dir %{_sysconfdir}/selinux
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/selinux/semanage.conf
%dir %{_libdir}/selinux
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

%files -n python-semanage
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_semanage.so
%{py_sitedir}/semanage.py[co]
%attr(755,root,root) %{_libdir}/selinux/semanage_migrate_store
