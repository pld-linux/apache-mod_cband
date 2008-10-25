%define		mod_name	cband
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: bandwidth limits per vhosts
Summary(pl.UTF-8):	Moduł do Apache: limity pasma dla poszczególnych vhostów
Name:		apache-mod_%{mod_name}
Version:	0.9.7.5
Release:	2
License:	Apache
Group:		Networking/Daemons/HTTP
Source0:	http://cband.linux.pl/download/mod-%{mod_name}-%{version}.tgz
# Source0-md5:	5c5d65dc9abe6cdc6931b6dd33be5018
Source1:	%{name}.conf
URL:		http://cband.linux.pl/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Requires:	crondaemon
Requires:	procps
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apacheconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d
%define		apachelibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)

%description
mod_cband is an Apache 2 module provided to solve the problem of
limiting users' and virtualhosts' bandwidth usage. When the configured
virtualhost's transfer limit is exceeded, mod_cband will redirect all
further requests to a location specified in the configuration file.

%description -l pl.UTF-8
mod_cband to moduł Apache'a 2 mający za zadanie ograniczanie zużycia
pasma przez użytkowników i hosty wirtualne. Gdy określony limit
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
install -d $RPM_BUILD_ROOT{%{apachelibdir},%{apacheconfdir}}

install src/.libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{apachelibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{apacheconfdir}/97_mod_%{mod_name}.conf

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/*mod_*.conf
%attr(755,root,root) %{apachelibdir}/*.so
