import subprocess
import re
import time

IP_RE = re.compile(r"\d+\.\d+\.\d+\.\d+")


def main():
    old_ips = set(get_ips())
    print "Running... will print on change"
    while True:
        print "."
        new_ips = set(get_ips())
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


def get_ips():
    cmd_str =
    nmap_ips = subprocess.check_output(["nmap -p 22 192.168.1.0/24 | grep open -B 4 | grep report"], shell=True)
    ips = []
    for line in nmap_ips.split('\n'):
        match = IP_RE.search(line)
        if match:
            ips.append(match.group(0))
    return ips


if __name__ == "__main__":
    main()
