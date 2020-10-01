import sys

from utils import subprocess_output
from config import get_configs

import argparse

parser = argparse.ArgumentParser(description='snmpbench')
parser.add_argument('hostname')
parser.add_argument('port', type=int)
parser.add_argument('--oid-batch-size', dest='oid_batch_size', type=int, default=10)
parser.add_argument('--sessions', dest='sessions', type=int, default=1)

args = parser.parse_args()

configs = get_configs(args.hostname, args.port, args.oid_batch_size, args.sessions)
results = []
for lib, config in configs.items():
    setup_cmd = config.get('setup')
    exec_cmd = config['exec']
    if setup_cmd:
        setup_res, stderr, code = subprocess_output(setup_cmd)
        if code != 0:
            raise Exception("stderr: {}".format(stderr.strip()))

    exec_res, exec_stderr, code = subprocess_output(exec_cmd)
    if code != 0:
        raise Exception("stderr: {}".format(stderr.strip()))

    exec_res = exec_res.decode('utf-8')
    for line in exec_res.split('\n'):
        if 'duration' in line:
            duration = line.split()[2]
            break
    else:
        raise Exception('No duration found')

    exec_stderr = exec_stderr.decode('utf-8')
    for line in exec_stderr.split('\n'):
        if 'Maximum resident set size' in line:
            max_rss = line.split(':')[1].strip()
            break
    else:
        raise Exception('No duration found')

    results.append({
        'name': lib,
        'duration': duration,
        'max_rss': max_rss,
    })

print("SNMP Benchmark")
print("oid_batch_size: {}".format(args.oid_batch_size))
print("{:10s}  {:>10s} {:>10s}".format("", "duration", "max_rss"))
for res in results:
    print("{:10s}: {:>10s} {:>10s}".format(res['name'], res['duration'], res['max_rss']))
