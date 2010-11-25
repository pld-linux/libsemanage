Summary:	An interface for SELinux management
Summary(pl.UTF-8):	Interfejs do zarządzania SELinuksem
Name:		libsemanage
Version:	2.0.45
Release:	3
License:	LGPL v2.1+
Group:		Libraries
#git clone http://oss.tresys.com/git/selinux.git
Source0:	http://userspace.selinuxproject.org/releases/current/devel/%{name}-%{version}.tar.gz
# Source0-md5:	f3ca65a97e919894ffa3252c9849038a
URL:		http://userspace.selinuxproject.org/trac/wiki
BuildRequires:	bison
BuildRequires:	bzip2-devel
BuildRequires:	flex
BuildRequires:	libselinux-devel >= 2.0.0
BuildRequires:	libsepol-devel >= 2.0.37
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	ustr-devel
Requires:	libselinux >= 2.0.0
Requires:	libsepol >= 2.0.37
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
%pyrequires_eq	python-libs

%description -n python-semanage
Python binding for semanage library.

%description -n python-semanage -l pl.UTF-8
Wiązania Pythona do biblioteki semanage.

%prep
%setup -q

%build
%{__make} -j1 all pywrap \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -fno-strict-aliasing"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install install-pywrap \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	SHLIBDIR=$RPM_BUILD_ROOT/%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT

# make symlink across / absolute
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
