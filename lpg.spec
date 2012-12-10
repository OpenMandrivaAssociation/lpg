%global    _version 2.0.17
%global    _compat_version 1.1.0

Name:      lpg
Version:   %{_version}
Release:   3
Summary:   LALR Parser Generator
Group:     Development/Java
# although the text of the licence isn't distributed with some of the source,
# the author has exlicitly stated that everything is covered under the EPL
# see: http://sourceforge.net/forum/forum.php?thread_id=3277926&forum_id=523519
License:   EPL
URL:       http://lpg.sourceforge.net/

Source0:   http://downloads.sourceforge.net/lpg/lpg-java-runtime-src-%{version}.zip
Source1:   http://downloads.sourceforge.net/lpg/lpg-generator-cpp-src-%{version}.zip
Source2:   http://downloads.sourceforge.net/lpg/lpg-generator-templates-%{version}.zip

# source archive for the java compat lib
Source3:   http://downloads.sourceforge.net/lpg/lpgdistribution-05-16-06.zip

# upstream does not provide a build script or manifest file for the java
# compat lib
Source4:   %{name}-build.xml
Source5:   %{name}-manifest.mf

# TODO: drop Source3, 4, 5 and obsolete the java-compat package when dependent
# projects are ported to LPG 2.x.x

# executable name in the bootstrap make target is wrong; sent upstream, see:
# https://sourceforge.net/tracker/?func=detail&aid=2794057&group_id=155963&atid=797881
Patch0:    %{name}-bootstrap-target.patch

# change build script to build the base jar with osgi bundle info
Patch1:    %{name}-osgi-jar.patch

%description
The LALR Parser Generator (LPG) is a tool for developing scanners and parsers
written in Java, C++ or C. Input is specified by BNF rules. LPG supports
backtracking (to resolve ambiguity), automatic AST generation and grammar
inheritance.

%package       java
Summary:       Java runtime library for LPG
Group:         Development/Java

BuildArch:     noarch

BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: ant-apache-regexp
Requires:      java
Requires:      jpackage-utils

%description   java
Java runtime library for parsers generated with the LALR Parser Generator
(LPG).

%package       java-compat
Version:       %{_compat_version}
Summary:       Compatibility Java runtime library for LPG 1.x
Group:         Development/Java

BuildArch:     noarch

BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: ant
Requires:      java
Requires:      jpackage-utils

%description   java-compat
Compatibility Java runtime library for parsers generated with the LALR Parser
Generator (LPG) 1.x.

%prep
%setup -q -T -c -n %{name}-%{version}

# because you can't use setup to unzip to subdirectories when your source
# archives do not create top level directories
unzip -qq %{SOURCE0} -d lpg-java-runtime
unzip -qq %{SOURCE1} -d lpg-generator-cpp
unzip -qq %{SOURCE2} -d lpg-generator-templates
chmod -Rf a+rX,u+w,g-w,o-w .

# setup java compat stuff
%setup -q -D -T -a 3 -n %{name}-%{version}
cp -p %{SOURCE4} lpgdistribution/build.xml
cp -p %{SOURCE5} lpgdistribution/MANIFEST.MF

# apply patches
%patch0 -p0 -b .orig
%patch1 -p0 -b .orig

%build
# build java stuff
(cd lpg-java-runtime && ant -f exportPlugin.xml)

# build java compat stuff
(cd lpgdistribution && ant)

# build native stuff
pushd lpg-generator-cpp/src

# ARCH just tells us what tools to use, so this can be the same on all arches
# we build twice in order to bootstrap the grammar parser
make clean install ARCH=linux_x86 \
  LOCAL_CFLAGS="%{optflags}" LOCAL_CXXFLAGS="%{optflags}"
make bootstrap ARCH=linux_x86
make clean install ARCH=linux_x86 \
  LOCAL_CFLAGS="%{optflags}" LOCAL_CXXFLAGS="%{optflags}"

popd

%install
rm -rf %{buildroot}

install -pD -T lpg-java-runtime/%{name}runtime.jar \
  %{buildroot}%{_javadir}/%{name}runtime-%{_version}.jar
install -pD -T lpgdistribution/%{name}javaruntime.jar \
  %{buildroot}%{_javadir}/%{name}javaruntime-%{_compat_version}.jar
install -pD -T lpg-generator-cpp/bin/%{name}-linux_x86 \
  %{buildroot}%{_bindir}/%{name}

# create unversioned symlinks to jars
(cd %{buildroot}%{_javadir} && for jar in *-%{_version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{_version}||g"`; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{_compat_version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{_compat_version}||g"`; done)

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc lpg-generator-templates/docs/*
%{_bindir}/%{name}

%files java
%defattr(-,root,root,-)
%doc lpg-java-runtime/Eclipse\ Public\ License\ -\ Version\ 1_0.htm
%{_javadir}/%{name}runtime*

%files java-compat
%defattr(-,root,root,-)
%doc lpg-java-runtime/Eclipse\ Public\ License\ -\ Version\ 1_0.htm
%{_javadir}/%{name}javaruntime*



%changelog
* Sun Nov 27 2011 Guilherme Moro <guilherme@mandriva.com> 2.0.17-3
+ Revision: 734061
- rebuild
- imported package lpg

  + Oden Eriksson <oeriksson@mandriva.com>
    - the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0.4-19mdv2010.0
+ Revision: 429870
- rebuild

* Mon Jul 28 2008 Thierry Vignaud <tv@mandriva.org> 0.4-18mdv2009.0
+ Revision: 251408
- rebuild

* Thu Jan 03 2008 Olivier Blin <blino@mandriva.org> 0.4-16mdv2008.1
+ Revision: 140933
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Mon Jan 15 2007 Lenny Cartier <lenny@mandriva.com> 0.4-16mdv2007.0
+ Revision: 109148
- Rebuild
- Import lpg

