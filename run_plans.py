import json

from utils import subprocess_output

run_bench_cmd = ['python', 'run_bench.py', 'localhost', '1161', '--oid-batch-size', '50', '--sessions', '1', '--rounds', '10', '--json']

raw_res, stderr, code = subprocess_output(run_bench_cmd)
if code != 0:
    raise Exception("stderr: {}".format(stderr.decode('utf-8').strip()))

results = json.loads(raw_res)
for res in results['results']:
    print(res)



