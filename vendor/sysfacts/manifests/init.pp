class sysfacts (
    $document_root = '/var/www/html/sysfacts',
    $port = '80',
) {

  class { 'apache':
    default_vhost => true,
  }

  apache::vhost { 'sysfacter.puppetlabs.vm':
    port        => $port,
    docroot     => $document_root,
    ssl         => false,
    require     => File["${document_root}/index.py"],
    directories => [
      {
        path            => $document_root,
        addhandlers     => [{ handler => 'cgi-script', extensions => ['.cgi', '.py']}],
        directoryindex  => ['index.html index.htm index.html index.py index.cgi'],
        options         => ['-Indexes', '+ExecCGI'],
      },
    ],
  }

  package { 'python-devel':
    ensure => present,
  }
  package { 'python-setuptools':
    ensure  => present,
    require => Package['python-devel'],
  }

  file { $document_root:
    ensure  => directory,
    owner   => $::apache::params::user,
    group   => $::apache::params::group,
  }

  file { "${document_root}/index.py":
    ensure  => present,
    owner   => $::apache::params::user,
    group   => $::apache::params::group,
    mode    => 755,
    content => template('sysfacts/www/sysfacts-report.py'),
    require => [
      Package['python-setuptools'],
    ],
  }

  file { "${document_root}/requirements.txt":
    ensure  => present,
    owner   => $::apache::params::user,
    group   => $::apache::params::group,
    mode    => 644,
    content => template('sysfacts/www/requirements.txt'),
  }

  # install required python libs for the app
  exec { 'easy_install pip':
    path        => ["/usr/bin", "/usr/sbin"],
  }
  exec { "pip install -r ${document_root}/requirements.txt":
    require     => Exec['easy_install pip'],
    subscribe   => File["${document_root}/requirements.txt"],
    path        => ["/usr/bin", "/usr/sbin"],
  }

  # allow http and https protocol on firewall
  firewall { '100 allow http and https access':
    port   => [80, 443],
    proto  => tcp,
    action => accept,
  }
}
