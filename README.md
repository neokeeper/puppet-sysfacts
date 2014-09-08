# Custom puppet node configuration

This is pure testing puppet configuration and thus it might not comply with best puppet practise.

## Usage

    $ gem install puppet-librarian puppet
    $ puppet-librarian install
    $ vagrant up <vm>

### TODO

* Rewrite sysfacter into puppet module
* Add Apache CGI vhost using the sysfacter module

## Development and contribution

Run puppet provision

    $ vagrant provision <vm>

Restart VM with puppet provision

    $ vagrant reload <vm> --provision
