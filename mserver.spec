%define version 0.5.5
%define release %mkrel 9

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



%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.5-9mdv2011.0
+ Revision: 620410
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0.5.5-8mdv2010.0
+ Revision: 430108
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 0.5.5-7mdv2009.0
+ Revision: 253049
- rebuild

* Thu Jan 03 2008 Olivier Blin <oblin@mandriva.com> 0.5.5-5mdv2008.1
+ Revision: 140966
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - import mserver


* Wed Sep 06 2006 Buchan Milne <bgmilne@mandriva.org> 0.5.5-5mdv2007.0
- Rebuild
- minor cleanups

* Mon Sep 19 2005 Buchan Milne <bgmilne@linux-mandrake.com> 0.5.5-4mdk
- annual rebuild
- gcc4 fixes (p4)
- misc requires fixes and cleanups

* Fri Oct 17 2003 Buchan Milne <bgmilne@linux-mandrake.com> 0.5.5-3mdk
- Rebuild for a bot
- errno fix

* Thu Sep 26 2002 Buchan Milne <bgmilne@cae.co.za> 0.5.5-2mdk
- s/168.0/168.1/g in mserver.conf to match changes in ICS default config

* Mon Aug 19 2002 Buchan Milne <bgmilne@cae.co.za> 0.5.5-1mdk
- Change package name to mserver (with provides/obsoletes just in case)
- Better default mserver.conf
- Many cleanups
- Fix init script
- Cooker time!

* Mon Apr 29 2002 Buchan Milne <bgmilne@cae.co.za> 0.5.5-0.2mdk
- Fix docs, bzip2 man pages, remove stupid defintions
- add defattr

* Wed Mar 13 2002 Buchan Milne <bgmilne@cae.co.za> 0.5.5-0.1mdk
- First Mandrake-ish release

* Tue Nov 9 1999 Willi Eigenmann <weigenmann@yahoo.com>
 - Release c-mserver-0.5.5-4.i386.rpm.
 - Paul Howarth submitted patches (Thank you very much Paul).
   His patches are based on release 2. Release 3 only had one minor change.
 - Changes to spec file to incorporate the change in release 3.
 - Cosmetic changes to spec file.

* Tue Nov 2 1999 Paul Howarth <paul@city-fan.org> c-mserver-0.5.5-2
 - Patched config.c to prevent insertion of null parameters into the parameter database
   when reading blank or comment-only lines in the configuration file.
 - Patched dial.c to get the linkup script working; the snprintf call used to
   build the command was overwriting the script name.
 - Cosmetic changes to spec file.

* Mon Sep 13 1999 Willi Eigenmann <weigenmann@yahoo.com>
 - Release c-mserver-0.5.5-3.i386.rpm
 - Change spec file not to replace /etc/rc.d/rc.firewall without a backup
   Thanks to Alan Sobey for letting me know.
 - c-mserver-0.5.5-2.i386.rpm was never released by me.

* Sat Aug 7 1999 Willi Eigenmann <weigenmann@yahoo.com>
 - Work on c-mserver-0.5.5-2.i386.rpm
 - Modified my sample in /usr/doc/c-mserver-0.0.5/sampleconf/mserver.conf.
 - Corrected some minor mistakes in the spec file.

* Fri Jul 30 1999 Willi Eigenmann <weigenmann@yahoo.com>
 - Begin work on c-mserver-0.5.5-1.i386.rpm (missed out on v0.5.3 and v0.5.4).
 - c-mserver-0.5.2-2.i386.rpm was never released by me. 
 - Implemented changes outlined in ChangeLog.
 - Changed URL in /usr/doc/c-mserver-0.5.5/README to reflect current address (Charles please change)
 - Corrected some minor mistakes in the spec file.

* Wed Jul 7 1999 Willi Eigenmann <weigenmann@yahoo.com>
 - Finalised c-mserver-0.5.2-2.i386.rpm
 - Added entry to /etc/services when c-mserver is installed. 

* Sat Jul 3 1999 Willi Eigenmann <weigenmann@yahoo.com>
 - Added %%changelog section to this spec file.
 - Made some cosmetic changes to c-mserver-0.5.2.spec file.
 - Use compound mkdir -p line instead of individual calls to mkdir.
 - Changed URL in /usr/doc/c-mserver-0.5.2/README to reflect current address
 - Changed *configure ac_default_prefix=/usr/local to ac_default_prefix=/usr/sbin
 - Added pppsetup V2.16.
 - Cleaned out /usr/doc/c-mserver-0.5.2 directory.
