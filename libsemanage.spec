Summary:	An interface for SELinux management
Summary(pl):	Interfejs do zarz±dzania SELinuksem
Name:		libsemanage
Version:	1.4
Release:	2
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://www.nsa.gov/selinux/archives/%{name}-%{version}.tgz
# Source0-md5:	063010d314da724b33de18883b71b8ee
URL:		http://www.nsa.gov/selinux/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libselinux-devel >= 1.28
BuildRequires:	libsepol-devel
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An interface for SELinux management.

%description -l pl
Interfejs do zarz±dzania SELinuksem.

%package devel
Summary:	Header files for libsemanage library
Summary(pl):	Pliki nag³ówkowe biblioteki libsemanage
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for libsemanage library.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe biblioteki libsemanage.

%package static
Summary:	Static version of libsemanage library
Summary(pl):	Statyczna wersja biblioteki libsemanage
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of libsemanage library.

%description static -l pl
Statyczna wersja biblioteki libsemanage.

%package -n python-semanage
Summary:	Python binding for semanage library
Summary(pl):	Wi±zania Pythona do biblioteki semanage
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-semanage
Python binding for semanage library.

%description -n python-semanage -l pl
Wi±zania Pythona do biblioteki semanage.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall -fno-strict-aliasing"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	SHLIBDIR=$RPM_BUILD_ROOT/%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT

# make symlink across / absolute
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib} ; echo libsemanage.so.*) \
	$RPM_BUILD_ROOT%{_libdir}/libsemanage.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) /%{_lib}/libsemanage.so.*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/selinux/semanage.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsemanage.so
%{_includedir}/semanage

%files static
%defattr(644,root,root,755)
%{_libdir}/libsemanage.a

%files -n python-semanage
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_semanage.so
%{py_sitedir}/semanage.py
