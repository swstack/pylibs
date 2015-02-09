import os
import sys
sys.path.append(os.getcwd())

from simpcli.simpcli import simpcli, command, positional_argument, optional_argument
import subprocess
import re
import time
import shlex

IP_RE = re.compile(r"\d+\.\d+\.\d+\.\d+")


#-----------------------------------------------------------------------------------------
# Internal
#-----------------------------------------------------------------------------------------
def _get_ips(network, port):
    try:
        nmap = subprocess.Popen(shlex.split("nmap -p %s %s" % (port, network)),
                            stdout=subprocess.PIPE)
        grep_open = subprocess.Popen(shlex.split('grep -B 4 open'),
                                     stdin=nmap.stdout,
                                     stdout=subprocess.PIPE)
        grep_report = subprocess.check_output(shlex.split('grep report'),
                                              stdin=grep_open.stdout)
    except subprocess.CalledProcessError:
        return []

    nmap.wait()
    grep_open.wait()

    ips = []
    for line in grep_report.split('\n'):
        match = IP_RE.search(line)
        if match:
            ips.append(match.group(0))
    return ips


#-----------------------------------------------------------------------------------------
# CLI
#-----------------------------------------------------------------------------------------
@optional_argument('network', description='Network to scan (example: 192.168.1.0/24)')
@positional_argument(description='Port #')
@command(description='Scan [network] for [port] availability')
def scan_port(port, network='192.168.1.0/24'):
    old_ips = set(_get_ips(network, port))
    print "Running... will print on change"
    while True:
        print "."
        new_ips = set(_get_ips(network, port))
        added = new_ips - old_ips
        removed = old_ips - new_ips
        old_ips = new_ips
        if added or removed:
            print "== %s ==" % time.ctime()
            for ip in added:
                print "+ %s" % ip
            for ip in removed:
                print "- %s" % ip
        time.sleep(1)


@optional_argument('network', description='Network to scan (example: 192.168.1.0/24)')
@positional_argument(description='Port #')
@command(description='List all hosts with open [port] on a [network]')
def list_hosts(port, network='192.168.1.0/24'):
    for ip in _get_ips(network, port):
        print ip


if __name__ == "__main__":
    simpcli.load()
    simpcli.execute()
