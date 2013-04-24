# ensure that apt update is run before any packages are installed
class apt {
  exec { "apt-update":
    command => "/usr/bin/apt-get update"
  }

  # Ensure apt-get update has been run before installing any packages
  Exec["apt-update"] -> Package <| |>

}

include apt

package { "build-essential":
    ensure => "installed"
}

package { "python-software-properties":
    ensure => "installed"
}

package { "git-core":
    ensure => "latest"
}

package { "vim":
    ensure => "latest"
}

package { "python-psycopg2":
    ensure => "latest"
}

package { "python-virtualenv":
    ensure => "latest"
}

package { "python-pip":
    ensure => "latest"
}

package { "python-dev":
    ensure => "latest"
}

package { "redis-server":
    ensure => "latest"
}

package { "dos2unix":
    ensure => "latest"
}

package {'supervisor':
    ensure => "latest",
    require => File['/var/log/celeryflower.log']
}

package {'wine':
    ensure => "latest",
}

class { "celery::server":
  requirements => "/vagrant/requirements.txt",
  require => Package['python-pip']
}

file { '/var/celery/tasks.py':
   ensure => 'link',
   target => '/usr/local/apps/growth-yield-batch/scripts/tasks.py',
}

file { "/usr/local/apps/growth-yield-batch/fvsbin/FVSpn.exe":
    ensure => "present",
}

file { "/usr/local/apps/growth-yield-batch/scripts/fvs":
    ensure => "present",
    mode   => 775,
}

file { "/usr/local/data/tasks.db":
    ensure => "present",
    owner  => "vagrant",
    group  => "celery",
    require => File['/usr/local/data'],
    mode   => 775,
}

file { "/usr/local/data":
    ensure => "directory",
    owner  => "celery",
    group  => "vagrant",
    mode   => 775,
}

file { "/usr/local/data/tmp":
    ensure => "directory",
    owner  => "celery",
    group  => "vagrant",
    mode   => 775,
}

file { "/usr/local/data/out":
    ensure => "directory",
    owner  => "celery",
    group  => "vagrant",
    mode   => 775,
}


file { "/root/.wine":
    # hack to "solve" ticket #14
    ensure => "directory",
    owner  => "celery",
    group  => "vagrant",
    mode   => 775,
}

file { "/home/celery":
    ensure => "directory",
    owner  => "celery",
    group  => "celery",
    mode   => 775,
}

file { "/usr/local/bin/fvs":
    ensure => "link",
    target => '/usr/local/apps/growth-yield-batch/scripts/fvs',
    mode   => 775,
}

file { "/usr/local/bin/fvsstatus":
    ensure => "link",
    target => '/usr/local/apps/growth-yield-batch/scripts/status.py',
    mode   => 775,
}

file { "/usr/local/bin/fvsbatch":
    ensure => "link",
    target => '/usr/local/apps/growth-yield-batch/scripts/batch.py',
    mode   => 775,
}

file { "celeryflower.conf":
  path => "/etc/supervisor/conf.d/celeryflower.conf",
  content => template("celeryflower.conf"),
  require => Package['supervisor']
}

file { "/var/log/celeryflower.log":
    ensure => "present",
    owner  => "celery",
    group  => "vagrant",
    mode   => 775,
}
