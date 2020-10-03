import json
from collections import defaultdict

from utils import subprocess_output


def get_results(oid_batch_size=50, sessions=1, rounds=1):
    run_bench_cmd = ['python', 'run_bench.py', 'localhost', '1161',
                     '--oid-batch-size', str(oid_batch_size),
                     '--sessions', str(sessions),
                     '--rounds', str(rounds),
                     '--json']
    raw_res, stderr, code = subprocess_output(run_bench_cmd)
    if code != 0:
        raise Exception("stderr: {}".format(stderr.decode('utf-8').strip()))
    return json.loads(raw_res)


session_results = {}
for i in [1, 10, 20, 50, 100, 150, 200]:
    kwargs = {
        'oid_batch_size': 50,
        'rounds': 1,
        'sessions': i,
    }
    print("Run for params: {}".format(kwargs))
    session_results[i] = get_results(**kwargs)

import matplotlib.pyplot as plt

names = [result['name'] for result in next(iter(session_results.values()))['results']]
sessions = session_results.keys()

per_lib = defaultdict(list)

for _, results in session_results.items():
    for result in results['results']:
        per_lib[result['name']].append(result['max_rss'])

for lib, values in per_lib.items():
    plt.plot(sessions, values, label=lib)

plt.xlabel('Sessions')
plt.ylabel('Max RSS (KBytes)')
plt.legend()
plt.savefig('docs/generated_images/max_rss_by_sessions.png', bbox_inches='tight')
