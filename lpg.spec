%define	name	lpg
%define	version	0.4
%define	release	%mkrel 20

Summary:	The LDP's Linux programming guide in HTML format
Name:		%name
Version:	%version
Release:	%release
Group:		Books/Computer books
Source:		%name-%version.html.tar.bz2
Url:		http://sunsite.unc.edu/LDP
License:	Artistic style
Buildroot:	%_tmppath/%name-%version-buildroot
BuildArch:	noarch

%description
The lpg package includes a generic guide for programming on Linux
systems, in HTML format.  You may want to check the Linux Documentation
Project's website at http://sunsite.unc.edu/LDP/ for more information and
possible updates to the programming guide.

If you'd like to view the Linux programming guide using your web browser
from files on your own machine, or if you'd like to provide it from your
web server, you should install the lpg package.

%prep
%setup -n %{name}

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_docdir/LDP/lpg
cp -ar * $RPM_BUILD_ROOT/%_docdir/LDP/lpg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%_docdir/LDP/lpg


