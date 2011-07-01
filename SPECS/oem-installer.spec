%define name    oem-installer
%define version 0.1 
%define release 1

Name:           %{name} 
Summary:        Powerfull tool to install recovery Mandriva OEM
Version:        %{version} 
Release:        %{release} 
Source0:        %{name}-%{version}.tar.bz2
URL:            http://github.com/jonatasteixeira/Mandriva-Installer

Group:          Applications
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot 
License:        GPLv2+
Buildarch:      noarch

BuildRequires:  python
BuildRequires:  python-qt4
#BuildRequires:  pygtk



%description
Powerfull tool to install mandriva oem, and recovery the system. The Python
script oem-installer get the informations about current system and starts the
installing or recovery procedure.


%prep 
%setup -q


%install
echo %{buildroot}
rm -rf %{buildroot}

%makeinstall

install -d -m 0755 %{buildroot}%{_sbindir}
install -d -m 0755 %{buildroot}%{_datadir}
install -d -m 0755 %{buildroot}%{_datadir}/%{name}
install -d -m 0755 %{buildroot}%{_datadir}/%{name}/app
install -d -m 0755 %{buildroot}%{_datadir}/%{name}/config
install -d -m 0755 %{buildroot}%{_datadir}/%{name}/lib
install -d -m 0755 %{buildroot}%{_datadir}/%{name}/resources
install -d -m 0755 %{buildroot}%{_datadir}/%{name}/script

#cp README.textile 	%{buildroot}/
#cp LICENSE 		%{buildroot}/
#cp AUTHORS 		%{buildroot}/

cp -rf tmp/%{name} 	%{buildroot}%{_sbindir}/%{name}
cp -rf app/* 		%{buildroot}%{_datadir}/%{name}/app/
cp -rf config/* 	%{buildroot}%{_datadir}/%{name}/config/
cp -rf lib/* 		%{buildroot}%{_datadir}/%{name}/lib/
cp -rf resources/* 	%{buildroot}%{_datadir}/%{name}/resources/
cp -rf script/* 	%{buildroot}%{_datadir}/%{name}/script/

%post

%clean 
rm -rf %{buildroot}
#rm -rf %{_sbindir}/%{name}
#rm -rf %{_datadir}/%{name}


%files 
%defattr(0755,root,root) 
#%doc README.textile LICENSE AUTHORS 
%{_sbindir}/%{name}
%{_datadir}/%{name}/*

