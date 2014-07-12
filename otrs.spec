Name:             otrs
Summary:          Web based ticket system
Version:          3.3.8
Release:          1%{?dist}
License:          AGPLv3
#Requires:     perl cronie httpd mod_perl procmail perl(Crypt::Eksblowfish::Bcrypt) perl(Date::Format) perl(DBI) perl(Encode::HanExtra) perl(IO::Socket::SSL) perl(JSON::XS) perl(GD::Graph) perl(GD::Text) perl(LWP::UserAgent) perl(Mail::IMAPClient) perl(Net::DNS) perl(Net::LDAP) perl(Net::SSL) perl(PDF::API2) perl(Sys::Syslog) perl(Text::CSV) perl(Text::CSV_XS) perl(Time::Piece) perl(URI) perl(version) perl(XML::Parser) perl(YAML::XS)
Source0:          http://ftp.otrs.org/pub/otrs/%{name}-%{version}.tar.bz2
Source1:          %{name}-httpd.conf
Source2:          %{name}-nginx.conf
BuildArch:        noarch

Requires:         %{name}-webserver = %{version}-%{release}
# TODO: add pgsql
Requires:         mysql-server

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildRequires:    systemd

Requires(pre):    shadow-utils

%package httpd
Summary:          Httpd integration for OTRS

Provides:         %{name}-webserver = %{version}-%{release}
Requires:         %{name} = %{version}-%{release}
Requires:         httpd

%description httpd
%{summary}.

%package nginx
Summary:          Nginx integration for OTRS

Provides:         %{name}-webserver = %{version}-%{release}
Requires:         %{name} = %{version}-%{release}
Requires:         nginx

%description nginx
%{summary}.

%description
Web based ticket system.
Feature list:
  Web-Interface:
    - Agent web interface for viewing and working on all customer requests
    - Admin web interface for changing system things
    - Customer web interface for viewing and sending infos to the agents
    - Webinterface with themes support
    - Multi language support (Brazilian Portuguese, Bulgarian, Dutch, English,
       Finnish, French, German, Italian and Spanish)
    - customize the output templates (dtl) release independently
    - Webinterface with attachment support
    - easy and logical to use
  Email-Interface:
    - PGP support
    - SMIME support
    - MIME support (attachments)
    - dispatching of incoming email via email addess or x-header
    - autoresponders for customers by incoming emails (per queue)
    - email-notification to the agent by new tickets, follow ups or lock timeouts
  Ticket:
    - custom queue view and queue view of all requests
    - Ticket locking
    - Ticket replies (standard responses)
    - Ticket autoresponders per queue
    - Ticket history, evolution of ticket status and actions taken on ticket
    - abaility to add notes (with different note types) to a ticket
    - Ticket zoom feature
    - Tickets can be bounced or forwarded to other email addresses
    - Ticket can be moved to a different queue (this is helpful if emails are
       for a specific subject)
    - Ticket priority
    - Ticket time accounting
    - Ticket merge feature
    - Ticket ACL support
    - content Fulltext search
  System:
    - creation and configuration of user accounts, and groups
    - creation of standard responses
    - Signature configuration per queue
    - Salutation configuration per queue
    - email-notification of administrators
    - email-notification sent to problem reporter (by create, locked, deleted,
       moved and closed)
    - submitting update-info (via email or webinterface).
    - deadlines for trouble tickets
    - ASP (activ service providing) support
    - TicketHook free setable like 'Call#', 'MyTicket#', 'Request#' or 'Ticket#'
    - Ticket number format free setable
    - different levels of permissions/access-rights.
    - central database, Support of different SQL databases (e. g. MySQL, PostgeSQL, ...)
    - user authentication agains database or ldap directory
    - easy to develope you own addon's (OTRS API)
    - easy to write different frontends (e. g. X11, console, ...)
    - own package manager (e. g. for application modules like webmail, calendar or
       filemanager)
    - a fast and usefull application

%prep
%setup -q
rm -rf var/fonts/
mv Custom/README Custom/README.custom
# config files
sed -i -e "s|/opt/otrs|%{_datadir}/%{name}|g" Kernel/Config.pm.dist
cp Kernel/Config.pm.dist Kernel/Config.pm
pushd Kernel/Config
  for foo in *.dist; do
    cp $foo `basename $foo .dist`
  done
popd
# crontab files
pushd var/cron
  for foo in *.dist; do
    mv $foo `basename $foo .dist`
  done
popd
# other files
cp .procmailrc.dist .procmailrc
cp .fetchmailrc.dist .fetchmailrc
cp .mailfilter.dist .mailfilter
# Use MySQL DB
sed -i \
    -e "s|/opt/otrs|/usr/share/%{name}|g" \
    -e "/mysql/s/^#use/use/g" \
    scripts/apache2-perl-startup.pl

%build
# Nothing to build

%install
install -Dpm 644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
install -Dpm 644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/nginx/conf.d/%{name}.conf
install -d -m 0755 %{buildroot}%{_datadir}/%{name}/
install -d -m 0755 %{buildroot}%{_datadir}/%{name}/Kernel/
install -d -m 0770 %{buildroot}%{_datadir}/%{name}/Kernel/Config/
install -d -m 0755 %{buildroot}%{_datadir}/%{name}/Custom/
install    -m 0660 Kernel/Config.pm \
                   %{buildroot}%{_datadir}/%{name}/Kernel/Config.pm
install    -m 0660 Kernel/Config/GenericAgent.pm \
                   %{buildroot}%{_datadir}/%{name}/Kernel/Config/GenericAgent.pm
install    -m 0640 .procmailrc \
                   %{buildroot}%{_datadir}/%{name}/.procmailrc
install    -m 0640 .fetchmailrc \
                   %{buildroot}%{_datadir}/%{name}/.fetchmailrc
install    -m 0640 .mailfilter \
                   %{buildroot}%{_datadir}/%{name}/.mailfilter
install    -m 0644 .procmailrc.dist \
                   %{buildroot}%{_datadir}/%{name}/.procmailrc.dist
install    -m 0644 .fetchmailrc.dist \
                   %{buildroot}%{_datadir}/%{name}/.fetchmailrc.dist
install    -m 0644 .mailfilter.dist \
                   %{buildroot}%{_datadir}/%{name}/.mailfilter.dist
mkdir -p %{buildroot}%{_pkgdocdir}
ln -sf %{_pkgdocdir}/README.custom \
      %{buildroot}%{_datadir}/%{name}/Custom/README
ln -sf %{_pkgdocdir}/GenericAgent.pm.examples \
      %{buildroot}%{_datadir}/%{name}/Kernel/Config/GenericAgent.pm.examples


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g apache -d %{_datadir}/%{name} -s /sbin/nologin \
    -c "OTRS System User" %{name}
exit 0

%post
# run OTRS rebuild config, delete cache, if the system was already in use (i.e. upgrade).
export OTRSUSER=otrs
if test -e %{_datadir}/%{name}/Kernel/Config/Files/ZZZAAuto.pm; then
    su $OTRSUSER -s /bin/bash -c %{_datadir}/%{name}/bin/otrs.RebuildConfig.pl;
    su $OTRSUSER -s /bin/bash -c %{_datadir}/%{name}/bin/otrs.DeleteCache.pl;
fi

%post httpd
%systemd_post httpd.service

%post nginx
%systemd_post nginx.service

%preun httpd
%systemd_preun httpd.service

%preun nginx
%systemd_preun nginx.service

%postun httpd
%systemd_postun_with_restart httpd.service

%postun nginx
%systemd_postun_with_restart nginx.service

%files httpd
%config %{_sysconfdir}/httpd/conf.d/%{name}.conf

%files nginx
%config %{_sysconfdir}/nginx/conf.d/%{name}.conf

%files
%doc AUTHORS.md CHANGES.md doc/ COPYING Custom/README.custom
%doc Kernel/Config/GenericAgent.pm.examples
# TODO: drop bundles
%doc COPYING-Third-Party

%config(noreplace) %{_datadir}/%{name}/Kernel/Config.pm
%config(noreplace) %{_datadir}/%{name}/Kernel/Config/GenericAgent.pm
#%config(noreplace) /opt/otrs/var/log/TicketCounter.log
%config(noreplace) %{_datadir}/%{name}/.procmailrc
%config(noreplace) %{_datadir}/%{name}/.fetchmailrc
%config(noreplace) %{_datadir}/%{name}/.mailfilter
#%config(noreplace) /opt/otrs/var/cron/*

%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/.procmailrc.dist
%{_datadir}/%{name}/.fetchmailrc.dist
%{_datadir}/%{name}/.mailfilter.dist
%{_datadir}/%{name}/Custom/
%{_datadir}/%{name}/Kernel/

%changelog
* Sat Jul 12 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.3.8-1
- Initial package
