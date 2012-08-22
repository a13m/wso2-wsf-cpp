%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo missing-httpd-devel)}}
%global pkg_name wso2-wsf-cpp
%global axis_name wso2-axis2
%global pkg_ver 2.1.0

%if 0%{?fedora} > 0
# Build/package everything on fedora
%global package_rampart 1
%global build_savan 1
%global build_sandesha2 1
%global build_wsclient 1
%global package_http_module 1
%global package_axis_http_server 1
%global package_axis2_modules 1
%else
%global package_rampart 0
%global build_savan 0
%global build_sandesha2 0
%global build_wsclient 0
%global package_http_module 0
%global package_axis_http_server 0
%global package_axis2_modules 0
%endif

Name: %{pkg_name}
Summary: WSO2 Web Services Framework for C++
Version: %{pkg_ver}
Release: 12.10%{?dist}
Group: Development/Tools
License: ASL 2.0
URL: http://wso2.org/library/wsf/cpp
# Original source tarball
#Source0: http://wso2.org/products/download/wsf/cpp/2.1.0/wso2-wsf-cpp-src-2.1.0.tar.gz
Source0: wso2-wsf-cpp-src-2.1.0-trimmed.tar.gz
Source1: wso2-trim-tarball.sh
# Remove minizip build references, used by wso2-trim-tarball.sh
Source2: wso2-nobuild-minizip.patch
# Remove sqlite3 build references, used by wso2-trim-tarball.sh
Source3: wso2-nobuild-sqlite3.patch
# Push DESTDIR to all installable components and allow proper setting of the
# libary install directory from configure
# https://wso2.org/jira/browse/WSFCPP-137
Patch0: wso2-build-fixes.patch
# Allow definition of library path for services
# https://issues.apache.org/jira/browse/AXIS2C-1544
Patch1: msg_rcvr_lib.patch
# Allow shared libs to be loaded using literal filenames as well as original inferred style
# https://issues.apache.org/jira/browse/AXIS2C-1549
Patch2: literal_lib_name.patch
# Make stream support more complete for SSL
# https://issues.apache.org/jira/browse/AXIS2C-1556
Patch3: generic_streams_for_ssl.patch
# Fix free of static buffer
# https://wso2.org/jira/browse/WSFCPP-138
Patch4: prevent_free_of_static_chars.patch
# 2.4 client_ip API change
# https://bugzilla.redhat.com/show_bug.cgi?id=833173
Patch5: 2.4_client_ip_API_change.patch
# Remove exit(0) calls in Environment.cpp for rpmlint
Patch6: remove_exit0_calls_for_rpmlint.patch
# https://issues.apache.org/jira/browse/AXIS2C-1522
Patch7: axis2c-curlinit.patch
# https://issues.apache.org/jira/browse/AXIS2C-1512
Patch8: axis2c-envpath.patch
# Fix linking DSO issues (is this upstream?)
Patch9: axis2c-dso.patch
# https://issues.apache.org/jira/browse/AXIS2C-1521
Patch10: axis2c-sslctx.patch
# Add missing data source checksum
# https://issues.apache.org/jira/browse/RAMPARTC-154
Patch11: rampartc-c14n-new.patch
# Fix two memory leaks
# https://issues.apache.org/jira/browse/RAMPARTC-153
# Patch12: rampartc-memleak.patch
# Fix bad timestamp checking (sent to upstream security list)
Patch13: rampartc-timestamp.patch

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: openssl-devel
BuildRequires: httpd-devel
BuildRequires: apr-devel
BuildRequires: libxml2-devel
BuildRequires: sqlite-devel
BuildRequires: dos2unix
Requires: %{axis_name} = %{version}-%{release}

%description
WSO2 Web Services Framework for C++. WSO2 WSF/C++ is a standards compliant,
enterprise grade, open source, C++ library for providing and consuming Web
services in C++. WSO2 WSF/C++ is a complete solution for building and
deploying Web services, and is the C++ library with a wide range of
WS-* specification implementations, including MTOM, WS-Addressing, WS-Policy,
WS-Security, WS-SecurityPolicy, WS-Reliable Messaging and WS-Events

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%doc README NEWS LICENSE NOTICE INSTALL README.INSTALL.LINUX README.SAMPLES
%_libdir/libwsf_cpp_msg_recv.so.*
%_libdir/libwso2_wsf.so.*
%_libdir/libneethi.so.*
%_libdir/libneethi_util.so.*

%package devel
Summary: WSO2 Web Services Framework for C++ development files
Group: Development/Tools
Requires: %{pkg_name} = %{version}-%{release}

%description devel
WSO2 Web Services Framework for C++. WSO2 WSF/C++ is a standards compliant,
enterprise grade, open source, C++ library for providing and consuming Web
services in C++. WSO2 WSF/C++ is a complete solution for building and
deploying Web services, and is the C++ library with a wide range of
WS-* specification implementations, including MTOM, WS-Addressing, WS-Policy,
WS-Security, WS-SecurityPolicy, WS-Reliable Messaging and WS-Events.

This package contains header files and documentation for developing with
the WSO2 Web Services Framework for C++

%files devel
%defattr(-,root,root)
%doc docs
%_includedir/%{pkg_name}/*.h
%_libdir/libwsf_cpp_msg_recv.so
%_libdir/libwso2_wsf.so
%_libdir/libneethi.so
%_libdir/libneethi_util.so

%if %{package_rampart}
%package -n %{pkg_name}-security
Summary: WSO2 Security for Web Services Framework for C++
Group: Development/Tools
Requires: wso2-rampart = %{version}-%{release}

%description -n %{pkg_name}-security
A security library for WSO2

%post -n %{pkg_name}-security
/sbin/ldconfig

%postun -n %{pkg_name}-security
/sbin/ldconfig

%files -n %{pkg_name}-security
%defattr(-,root,root)
%doc LICENSE
%_libdir/libwso2_wsf_security.so.*

%package -n %{pkg_name}-security-devel
Summary: WSO2 Security for Web Services Framework for C++
Group: Development/Tools
Requires: %{pkg_name}-security = %{version}-%{release}
Requires: %{pkg_name}-devel = %{version}-%{release}
Requires: wso2-rampart-devel = %{version}-%{release}

%description -n %{pkg_name}-security-devel
A security library for WSO2 development

%files -n %{pkg_name}-security-devel
%defattr(-,root,root)
%doc LICENSE
%_libdir/libwso2_wsf_security.so
%endif

%if %{build_wsclient}
%package -n wso2-wsclient
Summary: A web service client 
Group: System Environment/Daemons
Requires: %{pkg_name} = %{pkg_ver}
Requires: %{axis_name} = %{pkg_ver}
Requires: wso2-rampart = %{pkg_ver}

%description -n wso2-wsclient
A Web Services client

%files -n wso2-wsclient
%defattr(-,root,root)
%doc wsf_c/wsclient/LICENSE wsf_c/wsclient/README wsf_c/wsclient/docs
%_bindir/wsclient
%endif

%if %{package_http_module}
%package -n mod_%{axis_name}
Summary: An Apache HTTPD module which adds axis2 support
Group: System Environment/Daemons
Requires: httpd
Requires: apr
Requires: httpd-mmn = %{_httpd_mmn}

%description -n mod_%{axis_name}
An Apache HTTPD module that adds support for axis2 WebServices.  This package
is a modified version of the module provided by the developers of WSO2

%files -n mod_%{axis_name}
%defattr(-,root,root)
%doc wsf_c/axis2c/LICENSE
%doc wsf_c/axis2c/src/core/transport/xmpp/samples/server/axis2.xml
%_libdir/httpd/modules/mod_axis2.so
%endif

%if %{package_axis2_modules}
%package -n %{axis_name}-modules
Summary: Modules for the WSO2 modified Apache Axis2/C
Group: Development/Tools
Requires: %{axis_name} = %{version}-%{release}

%description -n %{axis_name}-modules
Apache Axis2/C is a Web services engine implementing the Axis2 architecture
in C.  Axis2/C can be used to provide and consume WebServices and supports
SOAP 1.1, 1.2, and REST style WebServices. Axis2/C also supports MTOM.

This package contains modules included in the Axis2/C distribution

%files -n %{axis_name}-modules
%defattr(-,root,root)
%doc wsf_c/axis2c/LICENSE wsf_c/axis2c/AUTHORS wsf_c/axis2c/CREDITS wsf_c/axis2c/INSTALL wsf_c/axis2c/NEWS wsf_c/axis2c/NOTICE wsf_c/axis2c/README
%_libdir/%{axis_name}/modules/addressing/libaxis2_mod_addr.so
%_libdir/%{axis_name}/modules/addressing/module.xml
%_libdir/%{axis_name}/modules/logging/libaxis2_mod_log.so
%_libdir/%{axis_name}/modules/logging/module.xml
%endif

%package -n %{axis_name}
Summary: WSO2 modified Apache Axis2/C
Group: Development/Tools
Requires: %{pkg_name} = %{version}-%{release}
Requires: pkgconfig

%description -n %{axis_name}
Apache Axis2/C is a Web services engine implementing the Axis2 architecture
in C.  Axis2/C can be used to provide and consume WebServices and supports
SOAP 1.1, 1.2, and REST style WebServices. Axis2/C also supports MTOM.

This package is a modified version of Apache Axis2/C provided by the
developers of WSO2

%post -n %{axis_name}
/sbin/ldconfig

%postun -n %{axis_name}
/sbin/ldconfig

%files -n %{axis_name}
%defattr(-,root,root)
%doc wsf_c/axis2c/LICENSE wsf_c/axis2c/AUTHORS wsf_c/axis2c/CREDITS wsf_c/axis2c/INSTALL wsf_c/axis2c/NEWS wsf_c/axis2c/NOTICE wsf_c/axis2c/README
%dir %_libdir/%{axis_name}/modules
%_libdir/libaxis2_axiom.so.*
%_libdir/libaxis2_engine.so.*
%_libdir/libaxis2_http_common.so.*
%_libdir/libaxis2_http_receiver.so.*
%_libdir/libaxis2_http_sender.so.*
%_libdir/libaxis2_parser.so.*
%_libdir/libaxis2_xpath.so.*
%_libdir/libaxutil.so.*
%_libdir/libguththila.so.*
%_bindir/tcpmon

%if %{package_axis_http_server}
%package -n %{axis_name}-http-server
Summary: WSO2's axis basic http server
Group: Development/Tools
Requires: %{axis_name} = %{pkg_ver}

%description -n %{axis_name}-http-server
The basic web server included as part of WSO2's axis

%files -n %{axis_name}-http-server
%defattr(-,root,root)
%doc wsf_c/axis2c/LICENSE
%_bindir/axis2_http_server
%endif

%package -n %{axis_name}-devel
Summary: WSO2's version of Apache Axis2/C development files
Group: Development/Tools
Requires: %{axis_name} = %{version}-%{release}

%description -n %{axis_name}-devel
Apache Axis2/C is a Web services engine implementing the Axis2 architecture
in C.  Axis2/C can be used to provide and consume WebServices and supports
SOAP 1.1, 1.2, and REST style WebServices. Axis2/C also supports MTOM.

This package contains header files and documentation for developing with
WSO2's version of Apache Axis2/C

%files -n %{axis_name}-devel
%defattr(-,root,root)
%doc wsf_c/docs/axis2c
%_includedir/axis2-1.6.0/*.h
%_includedir/axis2-1.6.0/platforms/*.h
%_includedir/axis2-1.6.0/platforms/unix/*.h
%_libdir/libaxis2_axiom.so
%_libdir/libaxis2_engine.so
%_libdir/libaxis2_http_common.so
%_libdir/libaxis2_http_receiver.so
%_libdir/libaxis2_http_sender.so
%_libdir/libaxis2_parser.so
%_libdir/libaxis2_xpath.so
%_libdir/libaxutil.so
%_libdir/libguththila.so
%_libdir/pkgconfig/axis2c.pc

%if %{package_rampart}
%package -n wso2-rampart
Summary: A security module for Apache Axis2/C
Group: Development/Tools
Requires: %{axis_name}
Requires: openssl

%description -n wso2-rampart
Apache Rampart/C is the security module for Apache Axis2/C featuring many
different means to secure SOAP messages including SOAP message encryption
and signature as specified in WS-Security Specification.  In addition Apache
Rampart/C configurations are based on security policy assertions as per
WS-Security Policy specification.

This package is a modified version of Apache Rampart/C provided by the
developers of WSO2

%post -n wso2-rampart
/sbin/ldconfig

%postun -n wso2-rampart
/sbin/ldconfig

%files -n wso2-rampart
%defattr(-,root,root)
%doc wsf_c/rampartc/LICENSE wsf_c/rampartc/AUTHORS wsf_c/rampartc/NEWS wsf_c/rampartc/NOTICE wsf_c/rampartc/README
%_libdir/librampart.so.*
%_libdir/%{axis_name}/modules/rahas/libmod_rahas.so
%_libdir/%{axis_name}/modules/rahas/module.xml
%_libdir/%{axis_name}/modules/rampart/libmod_rampart.so
%_libdir/%{axis_name}/modules/rampart/module.xml

%package -n wso2-rampart-devel
Summary: WSO2's version of Apache Rampart/C development files
Group: Development/Tools
Requires: wso2-rampart = %{version}-%{release}

%description -n wso2-rampart-devel
Apache Rampart/C is the security module for Apache Axis2/C featuring many
different means to secure SOAP messages including SOAP message encryption
and signature as specified in WS-Security Specification.  In addition Apache
Rampart/C configurations are based on security policy assertions as per
WS-Security Policy specification.

This package contains header files and documentation for developing with
WSO2's version of Apache Rampart/C

%files -n wso2-rampart-devel
%defattr(-,root,root)
%doc wsf_c/docs/rampartc
%_includedir/rampart-1.3.0/*.h
%_libdir/librampart.so
%endif

%if %{build_savan}
%package -n wso2-savan
Summary: A C implementation of the WS-Eventing specification
Group: Development/Tools
Requires: %{axis_name}

%description -n wso2-savan
Apache Savan/C is a C implementation of the WS-Eventing specification which is
built on top of Axis2/C.  Savan/C adds WS-Eventing capability to Web services
hosted using Axis2/C.

This package is a modified version of Apache Savan/C provided by the
developers of WSO2

%post -n wso2-savan
/sbin/ldconfig

%postun -n wso2-savan
/sbin/ldconfig

%files -n wso2-savan
%defattr(-,root,root)
%doc wsf_c/savanc/LICENSE wsf_c/savanc/AUTHORS wsf_c/savanc/INSTALL wsf_c/savanc/NEWS wsf_c/savanc/README
%_libdir/libsavan_client.so.*
%_libdir/libsavan_msgreceivers.so.*
%_libdir/libsavan_subs_mgr.so.*
%_libdir/libsavan_util.so.*
%_libdir/%{axis_name}/modules/savan/libmod_savan.so
%_libdir/%{axis_name}/modules/savan/module.xml

%package -n wso2-savan-devel
Summary: WSO2's version of Apache Savan/C development files
Group: Development/Tools
Requires: wso2-savan = %{version}-%{release}

%description -n wso2-savan-devel
Apache Savan/C is a C implementation of the WS-Eventing specification which is
built on top of Axis2/C.  Savan/C adds WS-Eventing capability to Web services
hosted using Axis2/C.

This package contains header files and documentation for developing with
WSO2's version of Apache Savan/C

%files -n wso2-savan-devel
%defattr(-,root,root)
%doc wsf_c/docs/savanc
%_includedir/savan-1.0/*.h
%_libdir/libsavan_client.so
%_libdir/libsavan_msgreceivers.so
%_libdir/libsavan_subs_mgr.so
%_libdir/libsavan_util.so
%endif

%if %{build_sandesha2}
%package -n wso2-sandesha2
Summary: A C implementation of WS-ReliableMessaging specification
Group: Development/Tools
Requires: %{axis_name}
Requires: sqlite

%description -n wso2-sandesha2
Apache Sandesha2/C is a C implementation of WS-ReliableMessaging specification
built on top of the Apache Axis2/C Web services engine.  Sandesha2/C adds
reliable messaging capability for Web services hosted using Axis2/C.
Sandesha2/C can also be used with an Axis2/C client to interact with already
hosted Web services in a reliable manner.

This package is a modified version of Apache Sandesha2/C provided by the
developers of WSO2

%post -n wso2-sandesha2
/sbin/ldconfig

%postun -n wso2-sandesha2
/sbin/ldconfig

%files -n wso2-sandesha2
%defattr(-,root,root)
%doc wsf_c/sandesha2c/LICENSE wsf_c/sandesha2c/AUTHORS wsf_c/sandesha2c/INSTALL wsf_c/sandesha2c/NEWS wsf_c/sandesha2c/README
%_libdir/libsandesha2_client.so.*
%_libdir/%{axis_name}/modules/sandesha2/libsandesha2.so
%_libdir/%{axis_name}/modules/sandesha2/module.xml

%package -n wso2-sandesha2-devel
Summary: WSO2's version of Apache Sandesha2/C development files
Group: Development/Tools
Requires: wso2-sandesha2 = %{version}-%{release}

%description -n wso2-sandesha2-devel
Apache Sandesha2/C is a C implementation of WS-ReliableMessaging specification
built on top of the Apache Axis2/C Web services engine.  Sandesha2/C adds
reliable messaging capability for Web services hosted using Axis2/C.
Sandesha2/C can also be used with an Axis2/C client to interact with already
hosted Web services in a reliable manner.

This package contains header files and documentation for developing with
WSO2's version of Apache Sandesha2/C

%files -n wso2-sandesha2-devel
%defattr(-,root,root)
%doc wsf_c/docs/sandesha2c
%_includedir/sandesha2-0.91/*.h
%_libdir/libsandesha2_client.so
%endif

%prep
%setup -q -n %{name}-src-%{version}
# Fix non-unix end-of-line characters in docs
dos2unix wsf_c/axis2c/NEWS
dos2unix wsf_c/axis2c/INSTALL
dos2unix wsf_c/axis2c/src/core/transport/xmpp/samples/server/axis2.xml
dos2unix docs/style.css
dos2unix NOTICE
dos2unix README
dos2unix NEWS

# Fix spurrious executable perms on doc files
chmod a-x wsf_c/docs/axis2c/*.cgi
%if %{package_rampart}
chmod a-x wsf_c/docs/rampartc/*.cgi
%endif
%if %{build_sandesha2}
chmod a-x wsf_c/docs/sandesha2c/*.cgi
%endif
%if %{build_savan}
chmod a-x wsf_c/docs/savanc/images/*.gif
chmod a-x wsf_c/docs/savanc/images/*.png
chmod a-x wsf_c/docs/savanc/images/logos/*.png
%endif
chmod a-x docs/api/html/installdox
%if %{build_wsclient}
chmod a-x wsf_c/wsclient/LICENSE
%endif

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
# %patch12 -p1
%patch13 -p1

%build
%if %{build_sandesha2}
sandesha2="--enable-sandesha"
%else
sandesha2="--disable-sandesha"
%endif

%if %{build_savan}
savan="--enable-savan"
%else
savan="--disable-savan"
%endif

%if %{build_wsclient}
wsclient="--enable-wsclient"
%else
wsclient="--disable-wsclient"
%endif

export CFLAGS="-O2 -D_FORTIFY_SOURCE=2 $RPM_OPT_FLAGS"
export CXXFLAGS=$CFLAGS
./configure --enable-multi-thread=no --with-axis2=`pwd`/wsf_c/axis2c/include --with-apache2=%{_includedir}/httpd --with-apr=%{_includedir}/apr-1 --with-sqlite=%{_includedir} --without-archive --enable-openssl --enable-libxml2 --disable-static --disable-rpath --bindir=%{_bindir} --sysconfdir=%{_sysconfdir} --libdir=%{_libdir} --includedir=%{_includedir} --datarootdir=%{_datadir}/%{pkg_name}-%{pkg_ver} --docdir=%{_datadir}/doc/%{pkg_name}-%{pkg_ver} --prefix=%{_prefix} $sandesha2 $savan $wsclient $rampart

# Remove rpath
find . -name libtool | xargs sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g'
find . -name libtool | xargs sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g'

make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Remove unneeded files
rm -rf %{buildroot}/%{_includedir}/axis2-1.6.0/platforms/windows
# This file is empty in the install.  It probably shouldn't be, but it's an
# issue with the installation script
rm -rf %{buildroot}/%{_prefix}/AUTHORS
# This is a duplicate of the LICENSE file
rm -rf %{buildroot}/%{_prefix}/COPYING
rm -rf %{buildroot}/%{_prefix}/LICENSE
# Remove the installed doc files.  The doc files are pulled from the build
# directory, not buildroot
rm -rf %{buildroot}/%{_prefix}/docs
rm -rf %{buildroot}/%{_datadir}/%{pkg_name}-%{pkg_ver}
rm -rf %{buildroot}/%{_prefix}/modules/sandesha2/LICENSE
rm -f %{buildroot}/%{_prefix}/CREDITS
rm -f %{buildroot}/%{_prefix}/INSTALL
rm -f %{buildroot}/%{_prefix}/LICENSE
rm -f %{buildroot}/%{_prefix}/NEWS
rm -f %{buildroot}/%{_prefix}/NOTICE
rm -f %{buildroot}/%{_prefix}/README
rm -f %{buildroot}/%{_prefix}/README.INSTALL.LINUX
rm -f %{buildroot}/%{_prefix}/README.SAMPLES
rm -f %{buildroot}/%{_prefix}/axis2.xml
# Remove libtool archives
rm -f %{buildroot}/%{_libdir}/*.la

# Fix the location and information in the pkgconfig
sed -i "s/lib64\/wso2-wsf-cpp/lib64/" %{buildroot}/%{_libdir}/pkgconfig/axis2c.pc

# Break into separate directories for packaging
%if %{package_http_module}
mkdir -p -m0755 %{buildroot}/%{_libdir}/httpd/modules
%endif
mkdir -p -m0755 %{buildroot}/%{_includedir}/%{pkg_name}
mkdir -p -m0755 %{buildroot}/%{_datadir}/%{pkg_name}
mkdir -p -m0755 %{buildroot}/%{_libdir}/%{axis_name}

%if !%{package_axis_http_server}
rm -f %{buildroot}/%{_prefix}/bin/axis2_http_server
%endif

# Move the modules directory
mv %{buildroot}/%{_prefix}/modules %{buildroot}/%{_libdir}/%{axis_name}

%if %{package_http_module}
# Fix the broken apache module names
pushd %{buildroot}/%{_libdir}
rm -f libmod_axis2.so libmod_axis2.so.0
mv -f libmod_axis2.so.0.6.0 mod_axis2.so
popd
mv -f %{buildroot}/%{_libdir}/mod_axis2.so %{buildroot}/%{_libdir}/httpd/modules
%else
rm -f %{buildroot}/%{_libdir}/libmod_axis2*
%endif

%if %{package_axis2_modules}
pushd %{buildroot}/%{_libdir}/%{axis_name}/modules/addressing
rm -f libaxis2_mod_addr.so libaxis2_mod_addr.so.0
rm -f libaxis2_mod_addr.la
mv -f libaxis2_mod_addr.so.0.6.0 libaxis2_mod_addr.so
popd
pushd %{buildroot}/%{_libdir}/%{axis_name}/modules/logging
rm -f libaxis2_mod_log.so libaxis2_mod_log.so.0
rm -f libaxis2_mod_log.la
mv -f libaxis2_mod_log.so.0.6.0 libaxis2_mod_log.so
popd
%else
rm -rf %{buildroot}/%{_libdir}/%{axis_name}/modules/addressing/*
rm -rf %{buildroot}/%{_libdir}/%{axis_name}/modules/logging/*
%endif
mv %{buildroot}/%{_bindir}/tools/tcpmon/* %{buildroot}/%{_bindir}

%if %{build_savan}
pushd %{buildroot}/%{_libdir}/%{axis_name}/modules/savan
rm -f libmod_savan.la *.so *.so.0
mv -f libmod_savan.so.0.0.0 libmod_savan.so
popd
%else
rm -f %{buildroot}/%{_libdir}/%{axis_name}/modules/savan/*
%endif

%if %{build_sandesha2}
pushd %{buildroot}/%{_libdir}/%{axis_name}/modules/sandesha2
rm -f libsandesha2.la *.so *.so.0
mv -f libsandesha2.so.0.0.0 libsandesha2.so
popd
%else
rm -f %{buildroot}/%{_libdir}/%{axis_name}/modules/sandesha2/*
%endif

%if %{package_rampart}
pushd %{buildroot}/%{_libdir}/%{axis_name}/modules/rampart
rm -f libmod_rampart.la *.so *.so.0
mv -f libmod_rampart.so.0.3.0 libmod_rampart.so
popd
pushd %{buildroot}/%{_libdir}/%{axis_name}/modules/rahas
rm -f libmod_rahas.la *.so *.so.0
mv -f libmod_rahas.so.0.3.0 libmod_rahas.so
popd
%else
rm -f %{buildroot}/%{_libdir}/%{axis_name}/modules/rampart/*
rm -f %{buildroot}/%{_libdir}/%{axis_name}/modules/rahas/*
rm -fr %{buildroot}/%{_includedir}/rampart-1.3.0
rm -fr %{buildroot}/%{_libdir}/librampart.*
rm -fr %{buildroot}/%{_libdir}/libwso2_wsf_security.*
%endif
mv -f %{buildroot}/%{_includedir}/*.h %{buildroot}/%{_includedir}/%{pkg_name}

%clean
rm -rf %{buildroot}

%changelog
* Thu Jul 19 2012 Andy Grimm <agrimm@gmail.com> - 2.1.0-12
- Integrate axis2/c & rampart/c patches from Eucalyptus and upstream

* Thu Jul 12 2012  Peter MacKinnon <pmackinn@redhat.com> - 2.1.0-11
- Added FORTIFY_SOURCE flag
- Added patch to remove exit(0) calls in wsf shared libs

* Thu Jul 12 2012  Peter MacKinnon <pmackinn@redhat.com> - 2.1.0-10
- Fixed typo in patch file

* Thu Jul 12 2012  Peter MacKinnon <pmackinn@redhat.com> - 2.1.0-9
- Added missing Requires: httpd-mmn

* Wed Jul 11 2012  Pete MacKinnon <pmackinn@redhat> - 2.1.0-8
- Added patch for 2.4 httpd API change

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-7
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 26 2011  Robert Rati <rrati@redhat> - 2.1.0-5
- Added patch to fix a free of a static buffer

* Tue Aug 16 2011  Robert Rati <rrati@redhat> - 2.1.0-4
- Added generic stream patch
- Created security package to separate rampart dependency

* Wed Apr 27 2011  Robert Rati <rrati@redhat> - 2.1.0-3
- Moved libmod* files to subdirs in %_libdir for appropriate loading into axis2
- Included default module.xml configs for axis2 modules, removed from doc
- Split Axis2/C modules into a separate package

* Mon Apr 25 2011  Robert Rati <rrati@redhat> - 2.1.0-2
- Improved library name loading issue in the engine

* Tue Apr 12 2011  Robert Rati <rrati@redhat> - 2.1.0-1
- Removed all libtool archives
- Removed codegen patch that wasn't built
- Added check for building on fedora
- Added upstream source URL
- Added BuildRequires for sqlite-devel
- Build from a trimmed tarball that excludes minizip and sqlite3
- Fixed httpd module packaging to be only axis2 modules

* Mon Apr 11 2011  Robert Rati <rrati@redhat> - 2.1.0-0.7
- Don't strip binaries, allow creation of debuginfo package
- Allow building of wsclient
- Removed rpath
- Added patch to allow configuration of library location for the engine

* Tue Apr  5 2011  Robert Rati <rrati@redhat> - 2.1.0-0.6
- Re-enabled setting want_sandesha2 and want_savan
- Removed want_axis2 and want_rampart flags.  They must be built
- Move axis2_http_server to its own package

* Tue Mar 15 2011  Robert Rati <rrati@redhat> - 2.1.0-0.5
- Fixed setting of libdir with configure

* Tue Mar 15 2011  Robert Rati <rrati@redhat> - 2.1.0-0.4
- Fixed rpmlint issues
- Moved libs out of subdirs
- Reorganized spec
- Added disable-savan and disable-sandesha to the configure line
- Enabled rampart
- Fixed axis2c dep

* Wed Mar 10 2011  Robert Rati <rrati@redhat> - 2.1.0-0.3
- Added option to control building the apache modules
- Added BuildRoot definition for older rpm versions

* Tue Mar  9 2011  Robert Rati <rrati@redhat> - 2.1.0-0.2
- Defaulted to only packaging the wso2 and axis related packages

* Tue Mar  9 2011  Robert Rati <rrati@redhat> - 2.1.0-0.1
- Inital packaging
