# TODO
# - should -libs Require main package?
# - drop binary-only nvidia-settings from here, and use nvidia-settings.spec for it?
# - kernel-drm is required on newer kernels. driver for kernel-longterm not requires drm
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# without kernel packages
%bcond_without	userspace	# don't build userspace programs
%bcond_with	settings	# package nvidia-settings here (GPL version of same packaged from nvidia-settings.spec)
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

# The goal here is to have main, userspace, package built once with
# simple release number, and only rebuild kernel packages with kernel
# version as part of release number, without the need to bump release
# with every kernel change.
%if 0%{?_pld_builder:1} && %{with kernel} && %{with userspace}
%{error:kernel and userspace cannot be built at the same time on PLD builders}
exit 1
%endif

%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%if 0%{?build_kernels:1}
%{error:alt_kernel and build_kernels are mutually exclusive}
exit 1
%endif
%undefine	with_userspace
%global		_build_kernels		%{alt_kernel}
%else
%global		_build_kernels		%{?build_kernels:,%{?build_kernels}}
%endif

%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		no_install_post_check_so 1

%define		kbrs	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo "BuildRequires:kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2" ; done)
%define		kpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%kernel_pkg ; done)
%define		bkpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%build_kernel_pkg ; done)

%define		rel	1
%define		mname	nvidia-legacy-304xx
%define		pname	xorg-driver-video-%{mname}
Summary:	Linux Drivers for nVidia GeForce/Quadro Chips
Summary(hu.UTF-8):	Linux meghajtók nVidia GeForce/Quadro chipekhez
Summary(pl.UTF-8):	Sterowniki do kart graficznych nVidia GeForce/Quadro
Name:		%{pname}%{?_pld_builder:%{?with_kernel:-kernel}}%{_alt_kernel}
Version:	304.121
Release:	%{rel}%{?_pld_builder:%{?with_kernel:@%{_kernel_ver_str}}}
Epoch:		1
License:	nVidia Binary
Group:		X11
Source0:	http://us.download.nvidia.com/XFree86/Linux-x86/%{version}/NVIDIA-Linux-x86-%{version}.run
# Source0-md5:	b8c950f0a30a6e1f503630fbd0ca8ab9
Source1:	http://us.download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}-no-compat32.run
# Source1-md5:	41e6d2b6325e5b0ae9889cfbd6bec696
Source2:	xinitrc.sh
Source3:	gl.pc.in
Source4:	10-nvidia.conf
Source5:	10-nvidia-modules.conf
Patch0:		X11-driver-nvidia-GL.patch
Patch1:		X11-driver-nvidia-desktop.patch
URL:		http://www.nvidia.com/object/unix.html
BuildRequires:	rpmbuild(macros) >= 1.678
%{?with_dist_kernel:%{expand:%kbrs}}
BuildRequires:	sed >= 4.0
BuildConflicts:	XFree86-nvidia
Requires:	%{pname}-libs = %{epoch}:%{version}-%{rel}
Requires:	xorg-xserver-server
Requires:	xorg-xserver-server(videodrv-abi) <= 15.0
Requires:	xorg-xserver-server(videodrv-abi) >= 2.0
Provides:	xorg-driver-video
Provides:	xorg-xserver-module(glx)
Obsoletes:	XFree86-driver-nvidia
Obsoletes:	XFree86-nvidia
Conflicts:	XFree86-OpenGL-devel <= 4.2.0-3
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{pname}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libnvcuvid.so
# libnvidia-encode.so.*.* links with libnvcuvid.so instead of libnvcuvid.so.1
%define		_noautoreq	libnvcuvid.so

%description
This driver set adds improved 2D functionality to the Xorg X server as
well as high performance OpenGL acceleration, AGP support, support for
most flat panels, and 2D multiple monitor support. Supported hardware:
modern NVIDIA GeForce (from GeForce2 MX) and Quadro (Quadro4 and up)
based graphics accelerators.

The older graphics chips are unsupported:
- NV1 and RIVA 128/128ZX chips are supported in the base Xorg install
  (nv driver)
- TNT/TNT2/GeForce 256/GeForce2 Ultra/Quadro2 are suported by -legacy
  drivers.

%description -l hu.UTF-8
Ez a meghajtó kibővíti az Xorg X szerver 2D működését OpenGL
gyorsítással, AGP támogatással és támogatja a több monitort.
Támogatott hardverek: modern NVIDIA GeForce (GeForce2 MX-től) és
Quadro (Quadro4 és újabbak) alapú grafikai gyorsítók.

A régekbbi grafikus chipek nem támogatottak:
- NV1 és RIVA 128/128ZX chipek az alap Xorg telepítéssel (nv meghajtó)
- TNT/TNT2/GeForce 256/GeForce2 Ultra/Quadro2 a -legacy driverekkel
  támogatottak.

%description -l pl.UTF-8
Usprawnione sterowniki dla kart graficznych nVidia do serwera Xorg,
dające wysokowydajną akcelerację OpenGL, obsługę AGP i wielu monitorów
2D. Obsługują w miarę nowe karty NVIDIA GeForce (od wersji GeForce2
MX) oraz Quadro (od wersji Quadro4).

Starsze układy graficzne nie są obsługiwane przez ten pakiet:
- NV1 i RIVA 128/128ZX są obsługiwane przez sterownik nv z Xorg
- TNT/TNT2/GeForce 256/GeForce 2 Ultra/Quadro 2 są obsługiwane przez
  sterowniki -legacy

%package libs
Summary:	OpenGL (GL and GLX) Nvidia libraries
Summary(pl.UTF-8):	Biblioteki OpenGL (GL i GLX) Nvidia
Group:		X11/Development/Libraries
Requires(post,postun):	/sbin/ldconfig
Requires:	libvdpau >= 0.3
Provides:	OpenGL = 2.1
Provides:	OpenGL-GLX = 1.4
Obsoletes:	X11-OpenGL-core < 1:7.0.0
Obsoletes:	X11-OpenGL-libGL < 1:7.0.0
Obsoletes:	XFree86-OpenGL-core < 1:7.0.0
Obsoletes:	XFree86-OpenGL-libGL < 1:7.0.0

%description libs
NVIDIA OpenGL (GL and GLX only) implementation libraries.

%description libs -l pl.UTF-8
Implementacja OpenGL (tylko GL i GLX) firmy NVIDIA.

%package devel
Summary:	OpenGL (GL and GLX) header files
Summary(hu.UTF-8):	OpenGL (GL és GLX) fejléc fájlok
Summary(pl.UTF-8):	Pliki nagłówkowe OpenGL (GL i GLX)
Group:		X11/Development/Libraries
Requires:	%{pname}-libs = %{epoch}:%{version}-%{rel}
Provides:	OpenGL-GLX-devel = 1.4
Provides:	OpenGL-devel = 2.1
Obsoletes:	X11-OpenGL-devel-base
Obsoletes:	XFree86-OpenGL-devel-base
Obsoletes:	XFree86-driver-nvidia-devel
Conflicts:	XFree86-OpenGL-devel < 4.3.99.902-0.3

%description devel
OpenGL header files (GL and GLX only) for NVIDIA OpenGL
implementation.

%description devel -l hu.UTF-8
OpenGL fejléc fájlok (csak GL és GLX) NVIDIA OpenGL implementációhoz.

%description devel -l pl.UTF-8
Pliki nagłówkowe OpenGL (tylko GL i GLX) dla implementacji OpenGL
firmy NVIDIA.

%package doc
Summary:	Documentation for NVIDIA Graphics Driver
Group:		Documentation

%description doc
NVIDIA Accelerated Linux Graphics Driver README and Installation
Guide.

%package progs
Summary:	Tools for advanced control of nVidia graphic cards
Summary(hu.UTF-8):	Eszközök az nVidia grafikus kártyák beállításához
Summary(pl.UTF-8):	Narzędzia do zarządzania kartami graficznymi nVidia
Group:		Applications/System
Requires:	%{pname} = %{epoch}:%{version}
Suggests:	pkgconfig
Obsoletes:	XFree86-driver-nvidia-progs

%description progs
Tools for advanced control of nVidia graphic cards.

%description progs -l hu.UTF-8
Eszközök az nVidia grafikus kártyák beállításához.

%description progs -l pl.UTF-8
Narzędzia do zarządzania kartami graficznymi nVidia.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-%{mname}\
Summary:	nVidia kernel module for nVidia Architecture support\
Summary(de.UTF-8):	Das nVidia-Kern-Modul für die nVidia-Architektur-Unterstützung\
Summary(hu.UTF-8):	nVidia Architektúra támogatás Linux kernelhez\
Summary(pl.UTF-8):	Moduł jądra dla obsługi kart graficznych nVidia\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
Requires:	dev >= 2.7.7-10\
%if %{with dist_kernel}\
%requires_releq_kernel\
%if %{_kernel_version_code} >= %{_kernel_version_magic 3 10 0}\
Requires:	%{releq_kernel -n drm}\
%endif\
Requires(postun):	%releq_kernel\
%endif\
Requires:	%{pname} = %{epoch}:%{version}\
Provides:	X11-driver-nvidia(kernel)\
Obsoletes:	XFree86-nvidia-kernel\
\
%description -n kernel%{_alt_kernel}-%{mname}\
nVidia Architecture support for Linux kernel.\
\
%description -n kernel%{_alt_kernel}-%{mname} -l de.UTF-8\
Die nVidia-Architektur-Unterstützung für den Linux-Kern.\
\
%description -n kernel%{_alt_kernel}-%{mname} -l hu.UTF-8\
nVidia Architektúra támogatás Linux kernelhez.\
\
%description -n kernel%{_alt_kernel}-%{mname} -l pl.UTF-8\
Obsługa architektury nVidia dla jądra Linuksa. Pakiet wymagany przez\
sterownik nVidii dla Xorg/XFree86.\
\
%files -n kernel%{_alt_kernel}-%{mname}\
%defattr(644,root,root,755)\
/lib/modules/%{_kernel_ver}/misc/*.ko*\
\
%post	-n kernel%{_alt_kernel}-%{mname}\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-%{mname}\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
cd kernel\
ln -sf Makefile.kbuild Makefile\
#cat >> Makefile <<'EOF'\
#\
#$(obj)/nv-kernel.o: $(src)/nv-kernel.o.bin\
#	cp $< $@\
#EOF\
#mv nv-kernel.o{,.bin}\
#build_kernel_modules -m nvidia\
%{__make} SYSSRC=%{_kernelsrcdir} clean\
ln -sf Makefile.kbuild Makefile\
%{__make} SYSSRC=%{_kernelsrcdir} module\
cd ..\
%install_kernel_modules -D installed -m kernel/nvidia -d misc\
%{nil}

%{?with_kernel:%{expand:%kpkg}}

%prep
cd %{_builddir}
rm -rf NVIDIA-Linux-x86*-%{version}*
%ifarch %{ix86}
/bin/sh %{SOURCE0} --extract-only
%setup -qDT -n NVIDIA-Linux-x86-%{version}
%else
/bin/sh %{SOURCE1} --extract-only
%setup -qDT -n NVIDIA-Linux-x86_64-%{version}-no-compat32
%endif
%patch0 -p1
%patch1 -p1

%build
%{?with_kernel:%{expand:%bkpkg}}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_libdir}/{nvidia,xorg/modules/{drivers,extensions/nvidia}} \
	$RPM_BUILD_ROOT{%{_includedir}/GL,%{_libdir}/vdpau,%{_bindir},%{_mandir}/man1} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},/etc/X11/xinit/xinitrc.d} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{OpenCL/vendors,ld.so.conf.d,X11/xorg.conf.d}

%if %{with settings}
install -p nvidia-settings $RPM_BUILD_ROOT%{_bindir}
cp -p nvidia-settings.1* $RPM_BUILD_ROOT%{_mandir}/man1
cp -p nvidia-settings.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -p nvidia-settings.png $RPM_BUILD_ROOT%{_pixmapsdir}
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d/nvidia-settings.sh
%endif

install -p nvidia-{smi,xconfig,bug-report.sh} $RPM_BUILD_ROOT%{_bindir}
cp -p nvidia-{smi,xconfig}.1* $RPM_BUILD_ROOT%{_mandir}/man1
install -p nvidia.icd $RPM_BUILD_ROOT%{_sysconfdir}/OpenCL/vendors

install %{SOURCE4} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
install %{SOURCE5} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
sed -i -e 's|@@LIBDIR@@|%{_libdir}|g' $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/10-nvidia-modules.conf

for f in \
	libGL.so.%{version}			\
	libOpenCL.so.1.0.0			\
	libcuda.so.%{version}			\
	libnvcuvid.so.%{version}		\
	libnvidia-cfg.so.%{version}		\
	libnvidia-compiler.so.%{version}	\
	libnvidia-glcore.so.%{version}		\
	libnvidia-ml.so.%{version}		\
	libnvidia-opencl.so.%{version}		\
	tls/libnvidia-tls.so.%{version}		\
; do
	install -p $f $RPM_BUILD_ROOT%{_libdir}/nvidia
done

install -p libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau

install -p libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia
ln -s libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libglx.so
install -p nvidia_drv.so $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/nvidia_drv.so.%{version}
ln -s nvidia_drv.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/nvidia_drv.so
install -p libnvidia-wfb.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia
ln -s libnvidia-wfb.so.1 $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libnvidia-wfb.so

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}/nvidia
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia

cp -p gl*.h $RPM_BUILD_ROOT%{_includedir}/GL

ln -sf libvdpau_nvidia.so.%{version} $RPM_BUILD_ROOT%{_libdir}/vdpau/libvdpau_nvidia.so.1

%ifarch %{x8664}
echo %{_libdir}/nvidia >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia64.conf
echo %{_libdir}/vdpau >>$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia64.conf
%else
echo %{_libdir}/nvidia >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
echo %{_libdir}/vdpau >>$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
%endif

# OpenGL ABI for Linux compatibility
ln -sf libGL.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libGL.so.1
ln -sf libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGL.so
ln -sf libOpenCL.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libOpenCL.so
ln -sf libcuda.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libcuda.so
ln -sf libnvcuvid.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libnvcuvid.so
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT
cp -a installed/* $RPM_BUILD_ROOT
%endif

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
sed -e '
	s|@@prefix@@|%{_prefix}|g;
	s|@@libdir@@|%{_libdir}|g;
	s|@@includedir@@|%{_includedir}|g;
	s|@@version@@|%{version}|g' < %{SOURCE3} \
	> $RPM_BUILD_ROOT%{_pkgconfigdir}/gl.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post
cat << 'EOF'
NOTE: You must also install kernel module for this driver to work:
  kernel%{_alt_kernel}-%{mname}-%{version}

EOF

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc LICENSE NVIDIA_Changelog README.txt
%dir %{_libdir}/xorg/modules/extensions/nvidia
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libnvidia-wfb.so.*.*
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libnvidia-wfb.so.1
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libnvidia-wfb.so
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libglx.so.*
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libglx.so
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/nvidia_drv.so.*
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/nvidia_drv.so
%{_sysconfdir}/X11/xorg.conf.d/10-nvidia.conf
%{_sysconfdir}/X11/xorg.conf.d/10-nvidia-modules.conf

%files libs
%defattr(644,root,root,755)
%dir %{_sysconfdir}/OpenCL
%dir %{_sysconfdir}/OpenCL/vendors
%{_sysconfdir}/OpenCL/vendors/nvidia.icd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld.so.conf.d/nvidia*.conf
%dir %{_libdir}/nvidia
%attr(755,root,root) %{_libdir}/nvidia/libGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGL.so.1
%attr(755,root,root) %{_libdir}/nvidia/libOpenCL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libOpenCL.so.1
%attr(755,root,root) %{_libdir}/nvidia/libOpenCL.so
%attr(755,root,root) %{_libdir}/nvidia/libcuda.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libcuda.so.1
%attr(755,root,root) %{_libdir}/nvidia/libcuda.so
%attr(755,root,root) %{_libdir}/nvidia/libnvcuvid.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvcuvid.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvcuvid.so
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-cfg.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-cfg.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-compiler.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-glcore.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-ml.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-ml.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-opencl.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libnvidia-opencl.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-tls.so.*.*
%attr(755,root,root) %{_libdir}/vdpau/libvdpau_nvidia.so.*.*
%attr(755,root,root) %ghost %{_libdir}/vdpau/libvdpau_nvidia.so.1

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/GL
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%attr(755,root,root) %{_libdir}/nvidia/libGL.so
%{_pkgconfigdir}/gl.pc

%files doc
%defattr(644,root,root,755)
%doc html/*

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nvidia-bug-report.sh
%attr(755,root,root) %{_bindir}/nvidia-smi
%attr(755,root,root) %{_bindir}/nvidia-xconfig
%{_mandir}/man1/nvidia-smi.1*
%{_mandir}/man1/nvidia-xconfig.1*
%if %{with settings}
%attr(755,root,root) /etc/X11/xinit/xinitrc.d/*.sh
%attr(755,root,root) %{_bindir}/nvidia-settings
%{_mandir}/man1/nvidia-settings.1*
%{_desktopdir}/nvidia-settings.desktop
%{_pixmapsdir}/nvidia-settings.png
%endif
%endif
