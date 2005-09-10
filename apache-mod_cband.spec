%define		mod_name	cband
%define 	apxs		/usr/sbin/apxs
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)

Summary:	Apache module: bandwidth limits per vhosts
Summary(pl):	Modu³ do Apache: limity pasma per vhosty
Name:		apache-mod_%{mod_name}
Version:	0.9.1
Release:	0.1
License:	Apache
Group:		Networking/Daemons
Source0:	http://cband.linux.pl/download/mod_%{mod_name}-%{version}.tgz
# Source0-md5:	8f00b72f194719ee99d52a6175a74dbb
Source1:	%{name}.conf
Source2:	%{name}.conf.examples
URL:		http://cband.linux.pl/
BuildRequires:	apache-devel >= 2.0.0
BuildRequires:	%{apxs}
Requires(post,preun):	%{apxs}
Requires(post,preun):	grep
Requires(preun):	fileutils
Requires:	apache >= 2.0.0
Requires:	crondaemon
Requires:	procps
Obsoletes:	apache-mod_%{mod_name} <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mod_cband is an Apache 2 module provided to solve the problem of
limiting users' and virtualhosts' bandwidth usage. When the configured
virtualhost's transfer limit is exceeded, mod_cband will redirect all
further requests to a location specified in the configuration file.

%description -l pl
mod_cband to modu³ maj±cy za zadanie ograniczanie zu¿ycia pasma przez
u¿ytkowników i virtualhostów. Gdy okre¶lony limit zostanie
przekroczony, mod_cband przekieruje wszelkie zapytania do strony
wskazanej w pliku konfiguracyjnym.

%prep
%setup -q -n mod_%{mod_name}-%{version}
cp %{SOURCE2} .

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/97_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.examples
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*mod_*.conf
%attr(755,root,root) %{_pkglibdir}/*
