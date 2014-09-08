node default {

  include repoforge
  include monit
  include apache

  package { 'fail2ban':
    ensure => present,
  }

  monit::process { 'fail2ban':
    ensure        => running,
    start_command => '/etc/init.d/fail2ban start',
    stop_command  => '/etc/init.d/fail2ban stop',
    pidfile       => '/var/run/fail2ban/fail2ban.pid',
    require       => Package['fail2ban'],
  }

  monit::process { 'apache':
    ensure        => running,
    start_command => '/etc/init.d/httpd start',
    stop_command  => '/etc/init.d/httpd stop',
    pidfile       => '/var/run/httpd/httpd.pid',
    require       => Package['httpd'],
  }
}
