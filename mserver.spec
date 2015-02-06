Summary:	C-Mserver Masqdialer daemon
Name:		mserver
Version:	0.5.5
Release:	13
License:	GPLv2+
Group:		Networking/Other
Url:		http://w3.cpwright.com/mserver
Source0:	ftp://ftp.cpwright.com:/pub/mserver/c-mserver-%{version}.tar.bz2
Source1:	mserver.pamd
Source2:	mserver.conf.bz2
Source3:	mserver.service
Patch0:		c-mserver-0.5.5-makefile.patch.bz2
Patch1:		mserver-0.5.5-config.patch.bz2
Patch2:		mserver-0.5.5-dial.patch.bz2
Patch3:		mserver-0.5.5-errno-fix.patch.bz2
Patch4:		mserver-0.5.5-gcc4-fixes.patch.bz2
Requires(pre):	rpm-helper sed
Provides:	c-mserver = %{EVRD}
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
The masqdialer system will allow authorized LAN users to manipulate
the network interface (usually a modem) that gives the Internet
access on a Linux box without having to use telnet. It's based on
a client/server approach so any TCP/IP enabled system should be able
to take advantage of this server, if a client is written for it.
Currently; Linux, Windows, NetBSD, and any system with a Java
implementation or Web Browser have clients.

Note: Please make changes to /etc/mserver.conf.

%files
%config(noreplace) %{_sysconfdir}/pam.d/mserver
%{_unitdir}/mserver.service
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

%post
%systemd_post mserver.service

# Add masqdialer entry to /etc/services if not already there
if ! ( grep ^[[:space:]]*224/tcp /etc/services > /dev/null ) then
       echo 'masqdialer      224/tcp		masqdialer	# added by c-mserver' >> /etc/services
fi
if ! ( grep ^[[:space:]]*224/udp /etc/services > /dev/null ) then
       echo 'masqdialer      224/udp		masqdialer	# added by c-mserver' >> /etc/services
fi

%preun
%systemd_preun mserver.service

%postun
%systemd_postun_with_restart mserver.service
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


#----------------------------------------------------------------------------

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

%configure2_5x
%make CPPFLAGS="%{optflags}"

%install
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/ppp
mkdir -p %{buildroot}/%{_mandir}/{man5,man8}
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
mkdir -p %{buildroot}%{_datadir}/mserver
install -m 755 mserver/mserver %{buildroot}%{_sbindir}/mserver
install -m 755 mchat/mchat %{buildroot}%{_sbindir}/mchat
install -m 755 authgen/authgen %{buildroot}%{_sbindir}/authgen
install -m 755 checkstat/findstat %{buildroot}%{_sbindir}/findstat
install -m 755 checkstat/checkstat %{buildroot}%{_sbindir}/checkstat
install -m 755 fakelink/linkcheck %{buildroot}%{_sbindir}/fakelink
install -m 755 fakelink/linkdown %{buildroot}%{_sbindir}/linkdown
install -m 755 fakelink/linkup %{buildroot}%{_sbindir}/linkup
install -m 664 pam/mserver %{buildroot}%{_sysconfdir}/pam.d/mserver
install -m 644 pppsetup/options.sample %{buildroot}%{_sysconfdir}/ppp/options.sample
install -m 755 pppsetup/ppp-off %{buildroot}%{_sbindir}
install -m 755 pppsetup/pppsetup %{buildroot}%{_sbindir}
install -D -p -m 0755 %{SOURCE3} %{buildroot}%{_unitdir}/mserver.service

bzcat %{SOURCE2}|sed -e 's/_VERSION_/%{version}/'> %{buildroot}/etc/mserver.conf
install -m 644 mchat/mchat.8 %{buildroot}/%{_mandir}/man8/mchat.8
install -m 644 docs/mserver.8 %{buildroot}/%{_mandir}/man8/mserver.8
install -m 644 docs/mserver.conf.5 %{buildroot}/%{_mandir}/man5/mserver.conf.5
