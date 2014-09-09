# Custom puppet node configuration

This is pure testing puppet configuration and thus it might not comply with best puppet practise.

Tested with <vm>: Centos6_64

## Usage

    $ gem install puppet-librarian puppet
    $ puppet-librarian install
    $ vagrant up <vm>

## Development and contribution

Run puppet provision

    $ vagrant provision <vm>

Restart VM with puppet provision

    $ vagrant reload <vm> --provision
