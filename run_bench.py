import sys

from utils import subprocess_output
from config import get_configs

hostname = sys.argv[1]
port = int(sys.argv[2])
oid_batch_size = int(sys.argv[3])

configs = get_configs(hostname, port, oid_batch_size)
results = []
for lib, config in configs.items():
    setup_cmd = config.get('setup')
    exec_cmd = config['exec']
    if setup_cmd:
        setup_res, stderr, code = subprocess_output(exec_cmd)
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
print("oid_batch_size: {}".format(oid_batch_size))
print("{:10s}  {:>10s} {:>10s}".format("", "duration", "max_rss"))
for res in results:
    print("{:10s}: {:>10s} {:>10s}".format(res['name'], res['duration'], res['max_rss']))
