%{?!ros_distro:%global ros_distro rolling}
%global pkg_name rc_genicam_driver
%global normalized_pkg_name %{lua:return (string.gsub(rpm.expand('%{pkg_name}'), '_', '-'))}

Name:           ros-rolling-rc-genicam-driver
Version:        0.3.0
Release:        3%{?dist}
Summary:        ROS %{pkg_name} package

License:        BSD
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  bloom-rpm-macros
BuildRequires:  cmake

%{?bloom_package}

%description
Driver for rc_visard and rc_cube from Roboception GmbH


%package devel
Release:        %{release}%{?release_suffix}
Summary:        %{summary}
Provides:       %{name} = %{version}-%{release}
Provides:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-runtime%{?_isa} = %{version}-%{release}

%description devel
Driver for rc_visard and rc_cube from Roboception GmbH


%package runtime
Release:        %{release}
Summary:        %{summary}

%description runtime
Driver for rc_visard and rc_cube from Roboception GmbH


%prep
%autosetup -p1


%generate_buildrequires
%bloom_buildrequires


%build
%cmake \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="%{bloom_prefix}" \
    -DAMENT_PREFIX_PATH="%{bloom_prefix}" \
    -DCMAKE_PREFIX_PATH="%{bloom_prefix}" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif

%cmake3_build


%install
%cmake_install


%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C %{__cmake_builddir} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
CTEST_OUTPUT_ON_FAILURE=1 \
    %cmake_build $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif


%files devel
%dir %{bloom_prefix}
%ghost %{bloom_prefix}/share/%{pkg_name}/package.xml


%files runtime
%{bloom_prefix}


%changelog
* Fri Mar 22 2024 Felix Ruess <felix.ruess@roboception.de> - 0.3.0-3
- Autogenerated by Bloom