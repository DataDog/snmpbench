import sys

from utils import subprocess_output
from config import get_configs

import argparse

parser = argparse.ArgumentParser(description='snmpbench')
parser.add_argument('hostname')
parser.add_argument('port', type=int)
parser.add_argument('--oid-batch-size', dest='oid_batch_size', type=int, default=10)
parser.add_argument('--sessions', dest='sessions', type=int, default=1)
parser.add_argument('--rounds', dest='rounds', type=int, default=1)
parser.add_argument('--print-results', dest='print_results', type=str, default='false')

args = parser.parse_args()

configs = get_configs(args.hostname, args.port, args.oid_batch_size, args.sessions, args.rounds, args.print_results)
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
        raise Exception("stderr: {}".format(exec_stderr.decode('utf-8').strip()))

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
print("sessions: {}".format(args.sessions))
print("rounds: {}".format(args.rounds))
print("print_results: {}".format(args.print_results))
print("{:10s}  {:>15s} {:>20s} {:>20s} {:>20s}".format("", "duration(ms)", "duration_per_oid", "max_rss(kbytes)", "rss_per_sess"))
for res in results:
    rss_per_sess = int(int(res['max_rss']) / args.sessions)
    duration_per_oid = float(res['duration']) / (args.sessions * args.oid_batch_size * args.rounds)
    print("{:10s}: {:>15s} {:>20f} {:>20s} {:>20d}".format(
        res['name'], res['duration'], duration_per_oid, res['max_rss'], rss_per_sess
    ))
