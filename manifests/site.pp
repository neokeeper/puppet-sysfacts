node default {

  # enable repoforge yum repository (incl. monit pkg)
  include repoforge

  # redefine monit default service check interval
  class { 'monit':
    check_interval  => 45,
  }

  package { 'fail2ban':
    ensure => present,
  }

  # fail2ban service monitoring using monit
  monit::process { 'fail2ban':
    ensure        => running,
    start_command => '/etc/init.d/fail2ban start',
    stop_command  => '/etc/init.d/fail2ban stop',
    pidfile       => '/var/run/fail2ban/fail2ban.pid',
    require       => Package['fail2ban'],
  }

  # apache service monitoring using monit
  monit::process { 'apache':
    ensure        => running,
    start_command => '/etc/init.d/httpd start',
    stop_command  => '/etc/init.d/httpd stop',
    timeout       => 30,
    pidfile       => '/var/run/httpd/httpd.pid',
    require       => Package['httpd'],
  }

  # install our stats & facts app under apache virtualhost
  include sysfacts
}
