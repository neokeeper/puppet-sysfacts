#!/usr/bin/env python
# coding: utf-8
# source: https://code.google.com/p/psutil/wiki/Documentation
# source: http://amitsaha.github.io/site/notes/articles/python_linux/article.html

from collections import namedtuple
import facter
import operator
import psutil

def net_devs_info():
    ''' RX and TX bytes for each of the network devices '''

    with open('/proc/net/dev') as f:
        # read information about network devices
        net_dump = f.readlines()

    device_data = {}
    data = namedtuple('data', ['rx', 'tx'])
    for line in net_dump[2:]:
        line = line.split(':')
        # skip localhost
        if line[0].strip() != 'lo':
            # save RX and TX stats for current network device
            device_data[line[0].strip()] = data(float(line[1].split()[0])/(1024.0*1024.0),
                                                float(line[1].split()[8])/(1024.0*1024.0))

    return device_data

def memory_info():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    meminfo = dict()

    with open('/proc/meminfo') as f:
        for line in f:
            # parse a line of meminfo
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo

class UniqueUser(set):
    def __call__(self, user):
        if user.name not in self:
            self.add(user.name)
            return True
        return False

def report_facts_and_stats():
    '''Print system statistics and information'''
    f = facter.Facter()

    # labels and facts mapping
    facts = {
        u'Architecture': 'architecture',
        u'System uptime': 'uptime',
        u'Timezone': 'timezone',
        u'SELinux': 'selinux',
        u'CPU count (physical)': 'physicalprocessorcount',
        u'CPU count (cores)': 'processorcount',
        u'Puppet version': 'puppetversion',
        u'OS family': 'osfamily',
        u'Kernel': 'kernelversion',
        u'IP address': 'ipaddress',
        u'Hostname': 'hostname',
        u'FQDN': 'fqdn',
        u'Type of hardware': 'virtual',
    }

    print
    print(u'== Basic facts ==')
    print

    # sort and print all facts based on mapping above
    for fact in sorted(facts.iteritems(), key=operator.itemgetter(1)):
        print(u'{0}: {1}'.format(fact[0], f.lookup(fact[1])))

    print
    print(u'== Additional information ==')
    print

    print(u'Running processes: {0}'.format(len(psutil.pids())))

    meminfo = memory_info()
    print('Total memory: {0}'.format(meminfo['MemTotal']))
    print('Free memory: {0}'.format(meminfo['MemFree']))

    netdevs = net_devs_info()
    for dev in netdevs.keys():
        print('{0}: RX {1:.2f} MiB, TX {2:.2f} MiB'.format(dev, netdevs[dev].rx, netdevs[dev].tx))

    opened_files = 0
    opened_sockets = 0
    examined_processes = 0
    for current_process in psutil.process_iter():
        try:
            # get count of file descriptors per this process
            opened_files += current_process.num_fds()
            # get count of socket connections per this process
            opened_sockets += len(current_process.connections('unix'))
            examined_processes += 1
        except psutil.NoSuchProcess:
            # process was terminated in intermediate time
            pass
        except psutil.AccessDenied:
            # current user running this script does not have sufficient permissions
            pass

    print(u'Opened files: {0} (the value might be only a partial statistic)'.format(opened_files))
    print(u'Opened sockets: {0} (the value might be only a partial statistic)'.format(opened_sockets))
    print(u'Examined processes: {0}'.format(examined_processes))

    print(u'Net connections: {0}'.format(len(psutil.net_connections())))

    print(u'System-wide CPU utilization (pct): {0}'.format(psutil.cpu_percent(interval=None)))

    print(u'User sessions: {0}'.format(len(psutil.users())))

    # group all sessions by unique owner (user) and get count of logged in unique users
    unique_users = filter(UniqueUser(), psutil.users())
    print(u'Logged in users (unique): {0}'.format(len(unique_users)))

if __name__=='__main__':

    report_facts_and_stats()
