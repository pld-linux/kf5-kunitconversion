#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.115
%define		qtver		5.15.2
%define		kfname		kunitconversion
#
Summary:	Converting physical units
Name:		kf5-%{kfname}
Version:	5.115.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	c01766f3867f156ae2869031be469a5f
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Network-devel
BuildRequires:	Qt5Test-devel
BuildRequires:	Qt5Xml-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	kf5-ki18n-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KUnitConversion provides functions to convert values in different
physical units. It supports converting different prefixes (e.g. kilo,
mega, giga) as well as converting between different unit systems (e.g.
liters, gallons). The following areas are supported:

- Acceleration
- Angle
- Area
- Currency
- Density
- Energy
- Force
- Frequency
- Fuel efficiency
- Length
- Mass
- Power
- Pressure
- Temperature
- Time
- Velocity
- Volume

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF5UnitConversion.so.5
%attr(755,root,root) %{_libdir}/libKF5UnitConversion.so.*.*.*
%{_datadir}/qlogging-categories5/kunitconversion.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KUnitConversion
%{_libdir}/cmake/KF5UnitConversion
%{_libdir}/libKF5UnitConversion.so
%{qt5dir}/mkspecs/modules/qt_KUnitConversion.pri
