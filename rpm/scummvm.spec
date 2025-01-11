%define disabled_engines testbed,playground3d,access
# build most popular/famous engines into the binary:
%define builtin_engines agi,agos,sci,scumm
# if --disable-all-engines is used, we need to enable sub engines manually:
%define sub_engines scumm-7-8,he,agos2,sci32,groovie2,lol,eob,mm1,xeen,ihnm,ultima1,ultima4,ultima6,ultima8,cstime,myst,mystme,riven

# Split other engines and data up into packages
# goal: ~5MB per package
%define engines_1 grim,kyra,mm,lure,sky,queen
%define engines_2 bladerunner,dm,drascula,gob,groovie,made,mohawk,myst3
%define engines_3 saga,stark,sword1,sword2,sword25,tinsel,titanic,tsage,twine
%define engines_4 glk,hugo,mads,sherlock,toltecs,wintermute,zvision
# separate packages because of size: ultima
%define dynamic_engines %{engines_1},%{engines_2},%{engines_3},%{engines_4},ultima

# replace commas with spaces for display (so we don't produce too long lines in descriptions
%define engines_1_pretty %{expand:%(echo %{engines_1} | tr ',' ' ' )}
%define engines_2_pretty %{expand:%(echo %{engines_2} | tr ',' ' ' )}
%define engines_3_pretty %{expand:%(echo %{engines_3} | tr ',' ' ' )}
%define engines_4_pretty %{expand:%(echo %{engines_4} | tr ',' ' ' )}

# build almost everything:
#%%define engine_config --disable-all-unstable-engines --disable-engine=%%{disabled_engines} --enable-engine-static=%%{builtin_engines}
# build only defined:
%define engine_config --disable-all-unstable-engines --disable-all-engines --disable-engine=%{disabled_engines} --enable-engine=%{sub_engines} --enable-engine-static=%{builtin_engines} --enable-engine-dynamic=%{dynamic_engines}
#%%define engine_config %%{nil}

# in order to quickly test building, make a lighter config via macro:
# You can set this to one of the following:
# - "configure-help" to print configure --help output
# - "die-configure"" to stop the build after the confgure phase
# - "die-build" to stop the build after compiling
# - "die-install" to stop the build after installing
%if 0%{?scummvm_quick:1}
%define engine_config --disable-all-engines --enable-engine-static=scumm --enable-engine-dynamic=sky
%endif

%global orgname org.scummvm.scummvm

# upstream sailfishos build recipe uses
# LDFLAGS "-Wl,-rpath,/usr/share/org.scummvm.scummvm/lib"
# so lets set up libdir accordingly.
# See configure below.
%define _plugindir %{_datadir}/%{orgname}/lib

%define config_opts_ext %{nil}
%ifarch %ix86
%define config_opts_ext --enable-ext-sse2
%endif
%ifarch %arm aarch64
%define config_opts_ext --enable-ext-neon
%endif


Name:       scummvm
Summary:    An interpreter for graphic adventure games
Version:    2.9.0
Release:    1
License:    GPLv3+
URL:        https://www.scummvm.org
Source0:    %{name}-%{version}.tar.xz
Source1:    scummvm.xpolicy
Source2:    scummvm.ini
Source3:    icon-launcher-scummvm.svg
Patch1:     0001-slash-separated-id.patch
Patch2:     0002-adapt-define-in-header.patch
Patch3:     0003-desktop.patch
# https://github.com/scummvm/scummvm/commit/0fe46dbebf4f89a6325f80316f189cb083589bd9.diff
Patch4:     2.9.0-fix-build-scummvmcloud-0fe46dbe.diff

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

BuildRequires:  sailfish-svg2png

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
BuildRequires:  pkgconfig(libmikmod)
BuildRequires:  pkgconfig(fluidsynth)
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

Other engines are packaged separately:

Engines I:   %engines_1_pretty

Engines II:  %engines_2_pretty

Engines III: %engines_3_pretty

Engines IV:  %engines_4_pretty

Ultima engine

See https://wiki.scummvm.org/index.php?title=Engines for details about engines
and game support.

# https://github.com/sailfishos-chum/main/blob/main/Metadata.md
%if "%{?vendor}" == "chum"
Title: ScummVM
Type: desktop-application
PackagedBy: nephros
Categories:
  - Game
  - Emulator
Custom:
  - Repo: https://github.com/scummvm/scummvm
PackageIcon: https://raw.githubusercontent.com/sailfishos-chum/sailfishos-scummvm/refs/heads/master/icons/svgs/icon-launcher-scummvm-scummvm.svg
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
%if "%{?vendor}" == "chum"
Requires:   soundfont-roland-sc55
%endif

%description data
%{summary}.

%if "%{?vendor}" == "chum"
Title: ScummVM Data
Type: addon
Categories:
  - Game
  - Emulator
PackageIcon: https://raw.githubusercontent.com/sailfishos-chum/sailfishos-scummvm/refs/heads/master/icons/svgs/icon-launcher-scummvm-retro2.svg
%endif

%package engines-i
Summary:    Engine plugins for ScummVM
Requires:   %{name} = %{version}-%{release}

%description engines-i
This package contains the following engine plugins: %{engines_1_pretty}

See https://wiki.scummvm.org/index.php?title=Engines for details about engines
and game support.

%if "%{?vendor}" == "chum"
Title: ScummVM Engines I
Type: desktop-application
Categories:
  - Game
  - Emulator
PackageIcon: https://raw.githubusercontent.com/sailfishos-chum/sailfishos-scummvm/refs/heads/master/icons/svgs/icon-launcher-scummvm-residual.svg
Screenshots:
  - https://scummvm.org/data/screenshots/grim/grim/grim_win_en_1_2_full.png
  - https://scummvm.org/data/screenshots/kyra/kyra1/kyra1_dos_en_1_1_full.png
  - https://scummvm.org/data/screenshots/mm/mm1/mm1_dos_en_1_1_full.png
  - https://scummvm.org/data/screenshots/lure/lure/lure_dos_en_1_3_full.png
  - https://scummvm.org/data/screenshots/sky/sky/sky_dos_en_1_1_full.png
  - https://scummvm.org/data/screenshots/queen/queen/queen_amiga_en_1_3_full.png
%endif

%package engines-ii
Summary:    Engine plugins for ScummVM
Requires:   %{name} = %{version}-%{release}

%description engines-ii
This package contains the following engine plugins: %{engines_2_pretty}

See https://wiki.scummvm.org/index.php?title=Engines for details about engines
and game support.


%if "%{?vendor}" == "chum"
Title: ScummVM Engines II
Type: desktop-application
Categories:
  - Game
  - Emulator
PackageIcon: https://raw.githubusercontent.com/sailfishos-chum/sailfishos-scummvm/refs/heads/master/icons/svgs/icon-launcher-scummvm-residual.svg
Screenshots:
  - https://scummvm.org/data/screenshots/bladerunner/bladerunner/bladerunner_win_en_1_1_full.png
  - https://upload.wikimedia.org/wikipedia/en/2/2b/Dungeon_Master_Gameplay_Screenshot.png
  - https://scummvm.org/data/screenshots/gob/gob1/gob1_dos_en_1_4_full.png
  - https://scummvm.org/data/screenshots/groovie/t7g/t7g_dos_en_1_2_full.png
  - https://scummvm.org/data/screenshots/made/lgop2/lgop2_dos_en_1_2_full.png
  - https://scummvm.org/data/screenshots/myst3/myst3/myst3_win_en_1_0_full.png
  - https://scummvm.org/data/screenshots/mohawk/mystme/mystme_win_de_1_2_full.png
%endif

%package engines-iii
Summary:    Engine plugins for ScummVM
Requires:   %{name} = %{version}-%{release}

%description engines-iii
This package contains the following engine plugins: %{engines_3_pretty}

See https://wiki.scummvm.org/index.php?title=Engines for details about engines
and game support.


%if "%{?vendor}" == "chum"
Title: ScummVM Engines III
Type: desktop-application
Categories:
  - Game
  - Emulator
PackageIcon: https://raw.githubusercontent.com/sailfishos-chum/sailfishos-scummvm/refs/heads/master/icons/svgs/icon-launcher-scummvm-residual.svg
Screenshots:
  - https://scummvm.org/data/screenshots/sword1/sword1/sword1_win_de_1_3_full.png
  - https://scummvm.org/data/screenshots/sword25/sword25/sword25_win_de_1_10_full.png
  - https://scummvm.org/data/screenshots/stark/tlj/tlj_win_en_1_0_full.png
  - https://scummvm.org/data/screenshots/titanic/titanic/titanic_win_en_1_2_full.png
  - https://scummvm.org/data/screenshots/tinsel/dw/dw_dos_en_1_1_full.png
%endif

%package engines-iv
Summary:    Engine plugins for ScummVM
Requires:   %{name} = %{version}-%{release}

%description engines-iv
This package contains the following engine plugins: %{engines_4_pretty}

See https://wiki.scummvm.org/index.php?title=Engines for details about engines
and game support.


%if "%{?vendor}" == "chum"
Title: ScummVM Engines IV
Type: desktop-application
Categories:
  - Game
  - Emulator
PackageIcon: https://raw.githubusercontent.com/sailfishos-chum/sailfishos-scummvm/refs/heads/master/icons/svgs/icon-launcher-scummvm-residual.svg
Screenshots:
  - https://scummvm.org/data/screenshots/toltecs/toltecs/toltecs_dos_en_1_6_full.png
  - https://scummvm.org/data/screenshots/sherlock/rosetattoo/rosetattoo_dos_de_1_13_full.png
  - https://scummvm.org/data/screenshots/zvision/znemesis/znemesis_dos_de_1_13_full.png
%endif

%package engines-ultima
Summary:    Engine plugins for ScummVM
Requires:   %{name} = %{version}-%{release}

%description engines-ultima
This package contains the following engine plugins: ultima

See https://wiki.scummvm.org/index.php?title=Engines for details about engines
and game support.


%if "%{?vendor}" == "chum"
Title: ScummVM Ultima Engine
Type: desktop-application
Categories:
  - Game
  - Emulator
PackageIcon: https://raw.githubusercontent.com/sailfishos-chum/sailfishos-scummvm/refs/heads/master/icons/svgs/icon-launcher-scummvm-residual.svg
Screenshots:
  - https://scummvm.org/data/screenshots/ultima/ultima4/ultima4_dos_en_1_1_full.png
  - https://scummvm.org/data/screenshots/ultima/ultima6/ultima6_dos_en_1_2_full.png
  - https://scummvm.org/data/screenshots/ultima/ultima8/ultima8_dos_en_2_1_full.png
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
PackageIcon: https://raw.githubusercontent.com/sailfishos-chum/sailfishos-scummvm/refs/heads/master/icons/svgs/icon-launcher-scummvm-retro-gr.svg
Categories:
  - Game
  - Emulator
%endif


%if "%{?vendor}" == "chum"
%package -n soundfont-roland-sc55
Summary:   Roland SC-55 MIDI SoundFont from ScummVM
BuildArch: noarch

%description -n soundfont-roland-sc55
Roland SC-55 soundfont from ScummVM

Title: Roland SC-55 MIDI SoundFont
Type: desktop-application
DeveloperName: deemster
Categories:
  - Audio
%endif


%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%if 0%{?scummvm_quick:1}
echo QUICK BUILD REQUEST. Defined minimal engine config. Packaging will likely fail.
%endif
%if "%{?scummvm_quick}" == "configure-help"
%configure --help
%endif

./configure \
--prefix=%{_prefix} --exec-prefix=%{_prefix} \
--libdir=%{_plugindir} \
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
--enable-scummvmdlc \
%{engine_config} \
%{config_opts_ext} \
#--enable-dlc \
%{nil}

%if "%{?scummvm_quick}" == "die-configure"
echo EXITING ON QUICK BUILD REQUEST. This was caused by the %%scummvm_quick macro.
exit 1
%endif

%make_build

%if "%{?scummvm_quick}" == "die-build"
echo EXITING ON QUICK BUILD REQUEST. This was caused by the %%scummvm_quick macro.
exit 1
%endif

%install
%make_install

rm -rf %{buildroot}%{_mandir}
# note that the configure script hard-codes this for sailfishos
rm -rf %{buildroot}%{_datadir}/%{orgname}/doc

mkdir -p %{buildroot}/usr/share/applications
cp dists/sailfish/org.scummvm.scummvm.desktop %{buildroot}/usr/share/applications/org.scummvm.scummvm.desktop

wd=$(date +%u) # 1-7
chosen=%{S:3}
if [ $wd -le 2 ]; then
chosen=%{_builddir}/%{name}-%{version}/icons/svgs/icon-launcher-scummvm-residual.svg
elif [ $wd -le 4 ]; then
chosen=%{_builddir}/%{name}-%{version}/icons/svgs/icon-launcher-scummvm-retro.svg
elif [ $wd -le 6 ]; then
chosen=%{_builddir}/%{name}-%{version}/icons/svgs/icon-launcher-scummvm-scummvm.svg
fi
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
cp $chosen %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/icon-launcher-scummvm.svg

# generate png icons
for size in 86 108 128 172 256 512 1024; do
install -d %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/
sailfish_svg2png -z 1.0 -f rgba -s 1 1 1 1 1 1 ${size} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/ %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/
done

mkdir -p %{buildroot}%{_sysconfdir}/pulse/xpolicy.conf.d/
cp %{S:1} %{buildroot}%{_sysconfdir}/pulse/xpolicy.conf.d/scummvm.conf


mkdir -p %{buildroot}%{_sysconfdir}/scummvm/
cp %{S:2} %{buildroot}%{_sysconfdir}/scummvm/scummvm.ini

%if "%{?vendor}" == "chum"
# built when FluidSynth was found:
mkdir -p %{buildroot}%{_datadir}/sounds/sf2
mv %{buildroot}%{_datadir}/%{orgname}/scummvm/Roland_SC-55.sf2 %{buildroot}%{_datadir}/sounds/sf2/Roland_SC-55.sf2
%endif


# Super duper hack on chum: read the log of our own build process:
%if "%{?vendor}" == "chum"
printf "This build of ScummVM includes the following engines:\n\n" > %{buildroot}%{_datadir}/%{orgname}/scummvm/built_engines_info.txt
printf "The following engines are built-in: %{builtin_engines}." >> %{buildroot}%{_datadir}/%{orgname}/scummvm/built_engines_info.txt
printf "These engines are packaged separately:\n\n" >> %{buildroot}%{_datadir}/%{orgname}/scummvm/built_engines_info.txt
printf "Engines I:   %{engines_1}\n" >> %{buildroot}%{_datadir}/%{orgname}/scummvm/built_engines_info.txt
printf "Engines II:  %{engines_2}\n" >> %{buildroot}%{_datadir}/%{orgname}/scummvm/built_engines_info.txt
printf "Engines III: %{engines_3}\n" >> %{buildroot}%{_datadir}/%{orgname}/scummvm/built_engines_info.txt
printf "Engines IV:  %{engines_4}\n" >> %{buildroot}%{_datadir}/%{orgname}/scummvm/built_engines_info.txt
printf "Ultima engine\n" >> %{buildroot}%{_datadir}/%{orgname}/scummvm/built_engines_info.txt
printf "\nThe above will include the following sub-engines: %{sub_engines}\n" >> %{buildroot}%{_datadir}/%{orgname}/scummvm/built_engines_info.txt
printf "\nSee https://wiki.scummvm.org/index.php?title=Engines for details about engines and game support.\n" >> %{buildroot}%{_datadir}/%{orgname}/scummvm/built_engines_info.txt

TOKEN1="Engines..builtin.:"
TOKEN2="Creating.engines\/engines.mk"
if [ -r %{_logdir}/build.log ]; then
  cat %{_logdir}/build.log | sed -n "/$TOKEN1/,/$TOKEN2/p" | sed -e "/$TOKEN1/d" -e "/$TOKEN2/d" | sed 's/^\[.*\]//' >> %{buildroot}%{_datadir}/%{orgname}/scummvm/built_engines_info.txt
elif [ -r //.build.log ]; then
  cat //.build.log         | sed -n "/$TOKEN1/,/$TOKEN2/p" | sed -e "/$TOKEN1/d" -e "/$TOKEN2/d" | sed 's/^\[.*\]//' >> %{buildroot}%{_datadir}/%{orgname}/scummvm/built_engines_info.txt
else
  printf "\nCould not get more info, please refer to the build log.\n\n" >> %{buildroot}%{_datadir}/%{orgname}/scummvm/built_engines_info.txt
fi
%endif

%if "%{?scummvm_quick}" == "die-install"
echo EXITING ON QUICK BUILD REQUEST. This was caused by the %%scummvm_quick macro.
exit 1
%endif


%files
%{_bindir}/*
%{_datadir}/applications/*.desktop
%config(noreplace) %{_sysconfdir}/scummvm/scummvm.ini
%config %{_sysconfdir}/pulse/xpolicy.conf.d/scummvm.conf
%{_datadir}/icons/hicolor/scalable/apps/*svg
%{_datadir}/icons/hicolor/*/apps/*.png
%exclude %{_datadir}/%{orgname}/applications/org.scummvm.scummvm.desktop
%exclude %{_datadir}/%{orgname}/icons/hicolor/scalable/apps/org.scummvm.scummvm.svg
%exclude %{_datadir}/%{orgname}/metainfo/org.scummvm.scummvm.metainfo.xml
%exclude %{_datadir}/%{orgname}/pixmaps/org.scummvm.scummvm.xpm
%dir %{_plugindir}/scummvm/
%if "%{?vendor}" == "chum"
%{_datadir}/%{orgname}/scummvm/built_engines_info.txt
%endif

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

%files engines-i
%{_plugindir}/scummvm/libgrim.so
%{_plugindir}/scummvm/libkyra.so
%{_plugindir}/scummvm/liblure.so
%{_plugindir}/scummvm/libmm.so
%{_plugindir}/scummvm/libqueen.so
%{_plugindir}/scummvm/libsky.so
%{_datadir}/%{orgname}/scummvm/grim-patch.lab
%{_datadir}/%{orgname}/scummvm/kyra.dat
%{_datadir}/%{orgname}/scummvm/lure.dat
%{_datadir}/%{orgname}/scummvm/mm.dat
%{_datadir}/%{orgname}/scummvm/queen.tbl
%{_datadir}/%{orgname}/scummvm/sky.cpt
%{_datadir}/%{orgname}/scummvm/shaders/grim_*
%{_datadir}/%{orgname}/scummvm/shaders/emi_*

%files engines-ii
%{_plugindir}/scummvm/libbladerunner.so
%{_plugindir}/scummvm/libdm.so
%{_plugindir}/scummvm/libdrascula.so
%{_plugindir}/scummvm/libgob.so
%{_plugindir}/scummvm/libgroovie.so
%{_plugindir}/scummvm/libmade.so
%{_plugindir}/scummvm/libmohawk.so
%{_plugindir}/scummvm/libmyst3.so
%{_datadir}/%{orgname}/scummvm/drascula.dat
%{_datadir}/%{orgname}/scummvm/myst3.dat
%{_datadir}/%{orgname}/scummvm/shaders/myst3_*

%files engines-iii
%{_plugindir}/scummvm/libsaga.so
%{_plugindir}/scummvm/libstark.so
%{_plugindir}/scummvm/libsword1.so
%{_plugindir}/scummvm/libsword2.so
%{_plugindir}/scummvm/libsword25.so
%{_plugindir}/scummvm/libtinsel.so
%{_plugindir}/scummvm/libtitanic.so
%{_plugindir}/scummvm/libtsage.so
%{_plugindir}/scummvm/libtwine.so
%{_datadir}/%{orgname}/scummvm/residualvm.zip
%{_datadir}/%{orgname}/scummvm/titanic.dat
%{_datadir}/%{orgname}/scummvm/shaders/stark_*

%files engines-iv
%{_plugindir}/scummvm/libglk.so
%{_plugindir}/scummvm/libhugo.so
%{_plugindir}/scummvm/libmads.so
%{_plugindir}/scummvm/libsherlock.so
%{_plugindir}/scummvm/libtoltecs.so
%{_plugindir}/scummvm/libwintermute.so
%{_plugindir}/scummvm/libzvision.so
%{_datadir}/%{orgname}/scummvm/hugo.dat
%{_datadir}/%{orgname}/scummvm/wintermute.zip
%{_datadir}/%{orgname}/scummvm/shaders/wme_*

%files engines-ultima
%{_plugindir}/scummvm/libultima.so
%{_datadir}/%{orgname}/scummvm/ultima.dat
%{_datadir}/%{orgname}/scummvm/ultima8.dat

%files fonts-cjk
%{_datadir}/%{orgname}/scummvm/fonts-cjk.dat

%if "%{?vendor}" == "chum"
%files -n soundfont-roland-sc55
%license dists/soundfonts/COPYRIGHT.Roland_SC-55
%{_datadir}/sounds/sf2/Roland_SC-55.sf2
%endif
