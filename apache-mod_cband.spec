%define		mod_name	cband
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: bandwidth limits per vhosts
Summary(pl):	Modu� do Apache: limity pasma dla poszczeg�lnych vhost�w
Name:		apache-mod_%{mod_name}
Version:	0.9.7.4
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://cband.linux.pl/download/mod-%{mod_name}-%{version}.tgz
# Source0-md5:	ff635d7b55bf7ca648d319247dfb45e3
Source1:	%{name}.conf
URL:		http://cband.linux.pl/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Requires:	crondaemon
Requires:	procps
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_cband is an Apache 2 module provided to solve the problem of
limiting users' and virtualhosts' bandwidth usage. When the configured
virtualhost's transfer limit is exceeded, mod_cband will redirect all
further requests to a location specified in the configuration file.

%description -l pl
mod_cband to modu� Apache'a 2 maj�cy za zadanie ograniczanie zu�ycia
pasma przez u�ytkownik�w i hosty wirtualne. Gdy okre�lony limit
zostanie przekroczony, mod_cband przekieruje wszelkie zapytania do
strony wskazanej w pliku konfiguracyjnym.

%prep
%setup -q -n mod-%{mod_name}-%{version}

%build
%configure \
	--with-apxs=%{apxs}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install src/.libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/97_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS Changes INSTALL conf/*.example
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*mod_*.conf
%attr(755,root,root) %{_pkglibdir}/*.so
