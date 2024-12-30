%define disabled_engines testbed,playground3d,access,zvision,wintermute
#%%define builtin_engines scumm
%define builtin_engines agi,agos,sci,scumm
# if --disable-all-engines is used, we need to enable sub engines manually:
%define sub_engines scumm-7-8,he,agos2,sci32,groovie2,lol,eob,mm1,xeen,ihnm,ultima1,ultima4,ultima6,ultima8,cstime,myst,mystme,riven
%define common_engines grim,kyra,mm,lure,sky,queen
%define extra_engines_1 bladerunner,dm,drascula,gob,groovie,made,mohawk,myst3
%define extra_engines_2 saga,stark,sword1,sword2,sword25,tinsel,titanic,tsage,twine,ultima
%define dynamic_engines %{common_engines},%{extra_engines_1},%{extra_engines_2}

# build almost everything:
#%%define engine_config --disable-all-unstable-engines --disable-engine=%%{disabled_engines} --enable-engine-static=%%{builtin_engines}
# build only defined:
%define engine_config --disable-all-unstable-engines --disable-all-engines --disable-engine=%{disabled_engines} --enable-engine=%{sub_engines} --enable-engine-static=%{builtin_engines} --enable-engine-dynamic=%{dynamic_engines}
#%%define engine_config %%{nil}

%global orgname org.scummvm.scummvm

%define config_opts_ext %{nil}
%ifarch %ix86
%define config_opts_ext --enable-ext-sse2
%endif
%ifarch %arm aarch64
%define config_opts_ext --enable-ext-neon
%endif


Name:       scummvm
Summary:    ScummVM
Version:    2.9.0
Release:    1
License:    GPLv3+
URL:        https://www.scummvm.org
Source0:    %{name}-%{version}.tar.xz
Source1:    scummvm.xpolicy
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  pkgconfig
BuildRequires:  gcc-c++
BuildRequires:  libstdc++-devel
BuildRequires:  git-core
BuildRequires:  curl
%ifarch %ix86
BuildRequires: nasm
%endif

BuildRequires:  giflib-devel
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  pkgconfig(libturbojpeg)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(readline)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_image)
#BuildRequires:  pkgconfig(SDL2_net)
BuildRequires:  SDL2_net-devel
BuildRequires:  pkgconfig(SDL2_ttf)
BuildRequires:  pkgconfig(egl)
#BuildRequires:  pkgconfig(glesv1_cm)
#BuildRequires:  libglvnd-devel # also provides glesv1_cm
BuildRequires:  mesa-llvmpipe-libGLESv1-devel
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(theoradec)
BuildRequires:  pkgconfig(zlib)

# libSDL deps
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-cursor)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: pkgconfig(wayland-scanner)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(libpulse-simple)

%if "%{?vendor}" == "chum"
BuildRequires:  pkgconfig(mad)
BuildRequires:  pkgconfig(libmpeg2)
%endif

Requires:   scummvm-data

%description
ScummVM is an interpreter that will play many graphic adventure games,
including LucasArts SCUMM games (such as Monkey Island 1-3, Day of the
Tentacle, Sam & Max, ...), many of Sierra's AGI and SCI games (such as King's
Quest 1-6, Space Quest 1-5, ...), Discworld 1 and 2, Simon the Sorcerer 1 and
2, Beneath A Steel Sky, Lure of the Temptress, Broken Sword 1 and 2, Flight of
the Amazon Queen, Gobliiins 1-3, The Legend of Kyrandia 1-3, many of Humongous
Entertainment's children's SCUMM games (including Freddi Fish and Putt Putt
games) and many more.

This package has the following engines built-in: %{builtin_engines}.
Other engines are packaged separately.

# https://github.com/sailfishos-chum/main/blob/main/Metadata.md
%if "%{?vendor}" == "chum"
Title: ScummVM
PackagedBy: nephros
Categories:
  - Game
  - Emulator
Custom:
  - Repo: https://github.com/scummvm/scummvm
PackageIcon: https://scummvm.org/images/scummvm_logo.png
Screenshots:
  - https://scummvm.org/data/screenshots/scumm/loom/loom_amiga_en_1_1_full.png
  - https://scummvm.org/data/screenshots/scumm/maniac/maniac_amiga_en_1_3_full.png
  - https://scummvm.org/data/screenshots/scumm/dig/dig_dos_en_1_2_full.png
  - https://scummvm.org/data/screenshots/scumm/monkey/monkey_dos_en_1_2_full.png
  - https://scummvm.org/data/screenshots/scumm/zak/zak_amiga_en_1_1_full.png
  - https://scummvm.org/data/screenshots/scumm/ft/ft_dos_en_1_5_full.png
Links:
  Homepage: %{url}
  Help: https://scummvm.org/contact
  Bugtracker: https://bugs.scummvm.org
%endif


%package data
Summary:   Core data files for ScummVM
BuildArch: noarch
Requires:   %{name} = %{version}-%{release}

%description data
%{summary}.

%if "%{?vendor}" == "chum"
Title: ScummVM Data
Type: addon
Categories:
  - Game
  - Emulator
%endif

%package engines-one
Summary:    Engine plugins for ScummVM
Requires:   %{name} = %{version}-%{release}

%description engines-one
This package contains the following engine plugins: %{common_engines}

%if "%{?vendor}" == "chum"
Title: ScummVM Engines I
Type: addon
Categories:
  - Game
  - Emulator
%endif

%package engines-two
Summary:    Additional engine plugins for ScummVM
Requires:   %{name} = %{version}-%{release}

%description engines-two
This package contains the following engine plugins: %{extra_engines_1}

%if "%{?vendor}" == "chum"
Title: ScummVM Engines II
Type: addon
Categories:
  - Game
  - Emulator
%endif

%package engines-three
Summary:    Additional engine plugins for ScummVM
Requires:   %{name} = %{version}-%{release}

%description engines-three
This package contains the following engine plugins: %{extra_engines_2}

%if "%{?vendor}" == "chum"
Title: ScummVM Engines III
Type: addon
Categories:
  - Game
  - Emulator
%endif

%package fonts-cjk
Summary:   CJK fonts for ScummVM
BuildArch: noarch
Requires:   %{name} = %{version}-%{release}

%description fonts-cjk
Chinese, Japanese, and Korean fonts for ScummVM

%if "%{?vendor}" == "chum"
Title: ScummVM CJK Fonts
Type: addon
Categories:
  - Game
  - Emulator
%endif


%prep
%autosetup -n %{name}-%{version}/upstream

%build
#%%configure --help

# upstream sailfishos build recipe uses
# LDFLAGS "-Wl,-rpath,/usr/share/org.scummvm.scummvm/lib"
# so lets set up libdir accordingly.

./configure \
--prefix=%{_prefix} --exec-prefix=%{_prefix} \
--libdir=%{_datadir}/%{orgname}/lib \
--mandir=%{_mandir} \
--host=sailfish \
--opengl-mode=any \
--disable-tinygl \
--disable-dependency-tracking \
--disable-detection-full \
--enable-release \
--enable-plugins \
--default-dynamic \
--no-builtin-resources \
--enable-vkeybd \
--disable-taskbar \
--disable-system-dialogs \
--disable-translation \
--disable-fribidi \
--disable-cloud \
--enable-text-console \
--enable-bink \
--disable-tremor \
--disable-libunity \
--disable-gtk \
--disable-discord \
--disable-enet \
%{engine_config} \
%{config_opts_ext} \
#--enable-dlc \
#--enable-scummvmdlc \
%{nil}

%make_build

%install
%make_install

rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_datadir}/%{orgname}/doc
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/icons/hicolor/86x86/apps
mkdir -p %{buildroot}/usr/share/icons/hicolor/108x108/apps
mkdir -p %{buildroot}/usr/share/icons/hicolor/128x128/apps
mkdir -p %{buildroot}/usr/share/icons/hicolor/172x172/apps
cp dists/sailfish/86x86.png   %{buildroot}/usr/share/icons/hicolor/86x86/apps/org.scummvm.scummvm.png
cp dists/sailfish/108x108.png %{buildroot}/usr/share/icons/hicolor/108x108/apps/org.scummvm.scummvm.png
cp dists/sailfish/128x128.png %{buildroot}/usr/share/icons/hicolor/128x128/apps/org.scummvm.scummvm.png
cp dists/sailfish/172x172.png %{buildroot}/usr/share/icons/hicolor/172x172/apps/org.scummvm.scummvm.png

cp dists/sailfish/org.scummvm.scummvm.desktop %{buildroot}/usr/share/applications/org.scummvm.scummvm.desktop
# FIXME
# Does the shipped X-Application key work with Sailjail??
sed -i -e 's/X-Application/X-Sailjail/g' %{buildroot}/usr/share/applications/org.scummvm.scummvm.desktop
# Custom Sailjail setup:
#printf '\n[X-Sailjail]\n' >> %%{buildroot}/usr/share/applications/org.scummvm.scummvm.desktop
#printf 'Sandboxing=Disabled\n' >> %%{buildroot}/usr/share/applications/org.scummvm.scummvm.desktop
#printf 'Permissions=Bluetooth;Downloads;PublicDir;RemovableMedia\n' >> %%{buildroot}/usr/share/applications/org.scummvm.scummvm.desktop
#printf "OrganizationName=%%{orgname}\n" >> %%{buildroot}/usr/share/applications/org.scummvm.scummvm.desktop
#printf 'ApplicationName=scummvm\n' >> %%{buildroot}/usr/share/applications/org.scummvm.scummvm.desktop

mkdir -p %{buildroot}%{_sysconfdir}/pulse/xpolicy.conf.d/
cp %{S:1} %{buildroot}%{_sysconfdir}/pulse/xpolicy.conf.d/scummvm.conf

%files
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_sysconfdir}/pulse/xpolicy.conf.d/scummvm.conf
#%%{_datadir}/icons/hicolor/scalable/apps/*svg
%{_datadir}/icons/hicolor/*/apps/*.png
%exclude %{_datadir}/%{orgname}/applications/org.scummvm.scummvm.desktop
%exclude %{_datadir}/%{orgname}/icons/hicolor/scalable/apps/org.scummvm.scummvm.svg
%exclude %{_datadir}/%{orgname}/metainfo/org.scummvm.scummvm.metainfo.xml
%exclude %{_datadir}/%{orgname}/pixmaps/org.scummvm.scummvm.xpm
# default/common engines
%dir %{_libdir}/scummvm/

%files data
%dir %{_datadir}/%{orgname}
%dir %{_datadir}/%{orgname}/scummvm/
%dir %{_datadir}/%{orgname}/scummvm/shaders/
# See dists/engine-data/README for usage:
%{_datadir}/%{orgname}/scummvm/shaders.dat
%{_datadir}/%{orgname}/scummvm/achievements.dat
%{_datadir}/%{orgname}/scummvm/encoding.dat
%{_datadir}/%{orgname}/scummvm/fonts.dat
%{_datadir}/%{orgname}/scummvm/gui-icons.dat
%{_datadir}/%{orgname}/scummvm/helpdialog.zip
%{_datadir}/%{orgname}/scummvm/pred.dic
%{_datadir}/%{orgname}/scummvm/scummclassic.zip
%{_datadir}/%{orgname}/scummvm/scummmodern.zip
%{_datadir}/%{orgname}/scummvm/scummremastered.zip
%{_datadir}/%{orgname}/scummvm/vkeybd_default.zip
%{_datadir}/%{orgname}/scummvm/vkeybd_small.zip
# we probably won't need these:
%exclude %{_datadir}/%{orgname}/scummvm/classicmacfonts.dat
%exclude %{_datadir}/%{orgname}/scummvm/macgui.dat
%exclude %{_datadir}/%{orgname}/scummvm/wwwroot.zip

%files engines-one
%{_libdir}/scummvm/libgrim.so
%{_libdir}/scummvm/libkyra.so
%{_libdir}/scummvm/liblure.so
%{_libdir}/scummvm/libmm.so
%{_libdir}/scummvm/libqueen.so
%{_libdir}/scummvm/libsky.so
%{_datadir}/%{orgname}/scummvm/grim-patch.lab
%{_datadir}/%{orgname}/scummvm/kyra.dat
%{_datadir}/%{orgname}/scummvm/lure.dat
%{_datadir}/%{orgname}/scummvm/mm.dat
%{_datadir}/%{orgname}/scummvm/queen.tbl
%{_datadir}/%{orgname}/scummvm/sky.cpt
%{_datadir}/%{orgname}/scummvm/shaders/grim_*
%{_datadir}/%{orgname}/scummvm/shaders/emi_*

%files engines-two
%{_libdir}/scummvm/libbladerunner.so
%{_libdir}/scummvm/libdm.so
%{_libdir}/scummvm/libdrascula.so
%{_libdir}/scummvm/libgob.so
%{_libdir}/scummvm/libgroovie.so
%{_libdir}/scummvm/libmade.so
%{_libdir}/scummvm/libmohawk.so
%{_libdir}/scummvm/libmyst3.so
%{_datadir}/%{orgname}/scummvm/drascula.dat
%{_datadir}/%{orgname}/scummvm/myst3.dat
%{_datadir}/%{orgname}/scummvm/shaders/myst3_*

%files engines-three
%{_libdir}/scummvm/libsaga.so
%{_libdir}/scummvm/libstark.so
%{_libdir}/scummvm/libsword1.so
%{_libdir}/scummvm/libsword2.so
%{_libdir}/scummvm/libsword25.so
%{_libdir}/scummvm/libtinsel.so
%{_libdir}/scummvm/libtitanic.so
%{_libdir}/scummvm/libtsage.so
%{_libdir}/scummvm/libtwine.so
%{_libdir}/scummvm/libultima.so
%{_datadir}/%{orgname}/scummvm/residualvm.zip
%{_datadir}/%{orgname}/scummvm/titanic.dat
%{_datadir}/%{orgname}/scummvm/ultima.dat
%{_datadir}/%{orgname}/scummvm/ultima8.dat
%{_datadir}/%{orgname}/scummvm/shaders/stark_*

%files fonts-cjk
%{_datadir}/%{orgname}/scummvm/fonts-cjk.dat

