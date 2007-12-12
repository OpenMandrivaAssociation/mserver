%define version 0.5.5
%define release %mkrel 5

Summary: 	C-Mserver Masqdialer daemon
Name: 		mserver
Version: 	%version
Release: 	%release
License: 	GPL
Group: 		Networking/Other
URL: 		http://w3.cpwright.com/mserver
Source: 	ftp://ftp.cpwright.com:/pub/mserver/c-mserver-%{version}.tar.bz2
Provides:	c-mserver
Obsoletes: 	c-mserver
Requires(pre):	rpm-helper sed
BuildRoot: 	%{_tmppath}/%{name}-%{version}
Source1:	mserver.pamd
Source2:	mserver.conf.bz2
Source3:	mserver.init
Patch0: 	c-mserver-%{version}-makefile.patch.bz2
Patch1: 	mserver-0.5.5-config.patch.bz2
Patch2: 	mserver-0.5.5-dial.patch.bz2
Patch3:		mserver-0.5.5-errno-fix.patch.bz2
Patch4:		mserver-0.5.5-gcc4-fixes.patch.bz2

%description
The masqdialer system will allow authorized LAN users to manipulate
the network interface (usually a modem) that gives the Internet
access on a Linux box without having to use telnet. It's based on
a client/server approach so any TCP/IP enabled system should be able
to take advantage of this server, if a client is written for it.
Currently; Linux, Windows, NetBSD, and any system with a Java
implementation or Web Browser have clients.

Note: Please make changes to /etc/mserver.conf.

%prep
%setup -q
%patch0 -p1
%patch1
%patch2
%patch3 -p1 -b .errno
%patch4 -p1 -b .gcc4

%build
#First clean up CVS files for rpmlint:
find . -name CVS -type d -exec rm -Rf {} \;|| true
find . -name .cvsignore -type f -exec rm -f {} \;|| true

%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/etc/ppp
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/{man5,man8}
mkdir -p $RPM_BUILD_ROOT/etc/pam.d
mkdir -p $RPM_BUILD_ROOT/usr/share/mserver
install -m 755 -s mserver/mserver $RPM_BUILD_ROOT%{_sbindir}/mserver
install -m 755 -s mchat/mchat $RPM_BUILD_ROOT%{_sbindir}/mchat
install -m 755 -s authgen/authgen $RPM_BUILD_ROOT%{_sbindir}/authgen
install -m 755 -s checkstat/findstat $RPM_BUILD_ROOT%{_sbindir}/findstat
install -m 755 -s checkstat/checkstat $RPM_BUILD_ROOT%{_sbindir}/checkstat
install -m 755 -s fakelink/linkcheck $RPM_BUILD_ROOT%{_sbindir}/fakelink
install -m 755 -s fakelink/linkdown $RPM_BUILD_ROOT%{_sbindir}/linkdown
install -m 755 -s fakelink/linkup $RPM_BUILD_ROOT%{_sbindir}/linkup
install -m 755 %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/mserver
install -m 664 pam/mserver $RPM_BUILD_ROOT/etc/pam.d/mserver
install -m 644 pppsetup/options.sample $RPM_BUILD_ROOT/etc/ppp/options.sample
install -m 755 pppsetup/ppp-off $RPM_BUILD_ROOT%{_sbindir}
install -m 755 pppsetup/pppsetup $RPM_BUILD_ROOT%{_sbindir}

bzcat %{SOURCE2}|sed -e 's/_VERSION_/%{version}/'> $RPM_BUILD_ROOT/etc/mserver.conf
install -m 644 mchat/mchat.8 $RPM_BUILD_ROOT/%{_mandir}/man8/mchat.8
install -m 644 docs/mserver.8 $RPM_BUILD_ROOT/%{_mandir}/man8/mserver.8
install -m 644 docs/mserver.conf.5 $RPM_BUILD_ROOT/%{_mandir}/man5/mserver.conf.5

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service mserver

# Add masqdialer entry to /etc/services if not already there
if ! ( grep ^[:space:]*224/tcp /etc/services > /dev/null ) then
       echo 'masqdialer      224/tcp	         masqdialer	# added by c-mserver' >> /etc/services
fi
if ! ( grep ^[:space:]*224/udp /etc/services > /dev/null ) then
       echo 'masqdialer      224/udp	         masqdialer	# added by c-mserver' >> /etc/services
fi

%preun
%_preun_service mserver

%postun
if [ $1 -eq 0 ]
    then
# Remove masqdialer entries from /etc/services
    cd /etc
    tmpfile=/etc/tmp.$$
    sed -e '/^[:space:]*masqdialer.*$/d' /etc/services > $tmpfile
    mv $tmpfile services
    sed -e '/^[:space:]*masqdialer.*$/d' /etc/services > $tmpfile
    mv $tmpfile services
fi

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pam.d/mserver
%{_sysconfdir}/rc.d/init.d/mserver
%config(noreplace) %{_sysconfdir}/ppp/options.sample
%{_sbindir}/mserver
%{_sbindir}/mchat
%{_sbindir}/authgen
%{_sbindir}/findstat
%{_sbindir}/checkstat
%{_sbindir}/fakelink
%{_sbindir}/linkdown
%{_sbindir}/linkup
%attr(0644,root,root) %{_mandir}/man5/mserver.conf.5*
%attr(0644,root,root) %{_mandir}/man8/mchat.8*
%attr(0644,root,root) %{_mandir}/man8/mserver.8*
%{_sbindir}/ppp-off
%{_sbindir}/pppsetup
%doc ChangeLog AUTHORS COPYING README
%doc docs/clients.html docs/doc.html docs/index.html
%doc docs/images sampleconf pppsetup firewallscripts/ipchainscripts

%attr(0644,root,root) %config(noreplace) /etc/mserver.conf

