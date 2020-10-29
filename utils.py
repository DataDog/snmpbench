import json
import subprocess
import tempfile
from collections import defaultdict
import matplotlib.pyplot as plt

class SubprocessOutputEmptyError(Exception):
    pass


def subprocess_output(command, raise_on_empty_output=False, env=None):
    """
    This is a stub to allow a check requiring `Popen` to run without an Agent (e.g. during tests or development),
    it's not supposed to be used anywhere outside the `datadog_checks.utils` package.
    """

    # Use tempfile, allowing a larger amount of memory. The subprocess.Popen
    # docs warn that the data read is buffered in memory. They suggest not to
    # use subprocess.PIPE if the data size is large or unlimited.
    with tempfile.TemporaryFile() as stdout_f, tempfile.TemporaryFile() as stderr_f:
        proc = subprocess.Popen(command, stdout=stdout_f, stderr=stderr_f, env=env)
        proc.wait()
        stderr_f.seek(0)
        err = stderr_f.read()
        stdout_f.seek(0)
        output = stdout_f.read()

    if not output and raise_on_empty_output:
        raise SubprocessOutputEmptyError("get_subprocess_output expected output but had none.")

    return output, err, proc.returncode


def get_results(oid_batch_size=50, session=1, round=1, snmp_version='2'):
    run_bench_cmd = ['python', 'run_bench.py', 'localhost', '1161',
                     '--oid-batch-size', str(oid_batch_size),
                     '--sessions', str(session),
                     '--rounds', str(round),
                     '--snmp-version', str(snmp_version),
                     '--json']
    raw_res, stderr, code = subprocess_output(run_bench_cmd)
    if code != 0:
        raise Exception("stderr: {}".format(stderr.decode('utf-8').strip()))
    return json.loads(raw_res)


def create_graph(session_results, column, column_desc, per_value, desc):
    sessions = session_results.keys()
    per_lib = defaultdict(list)
    for _, results in session_results.items():
        for result in results['results']:
            per_lib[result['name']].append(result[column])
    for lib, values in per_lib.items():
        plt.plot(sessions, values, label=lib)

    snmp_version = list(session_results.values())[0]['config']['snmp_version']
    plt.xlabel(per_value)
    plt.ylabel(column_desc)
    plt.legend()
    plt.title("{} per {}\n{}".format(column, per_value, desc))
    file_prefix = 'docs/generated_data/{}_{}_version{}'.format(per_value, column, snmp_version)
    fig_path = '{}.png'.format(file_prefix)
    data_path = '{}.json'.format(file_prefix)
    print("Save fig to: ", fig_path)
    print("Save data to: ", data_path)
    plt.savefig(fig_path, bbox_inches='tight')
    with open(data_path.format(file_prefix), 'w') as f:
        f.write(json.dumps(session_results, indent=4, sort_keys=True))

    plt.clf()


def create_all_graphs(session_results, per_value, desc=''):
    columns = {
        'max_rss': {
            'desc': 'Max RSS (KBytes)',
        },
        'user_time': {
            'desc': 'User time (sec)',
        },
        'sys_time': {
            'desc': 'System time (sec)',
        },
        'elapsed_time': {
            'desc': 'Elapsed (wall clock) time (sec)',
        },
        'duration_per_oid': {
            'desc': 'Duration Per OID (ms)',
        },
        'percent_cpu': {
            'desc': 'Percent CPU',
        },
        'minor_page_faults': {
            'desc': 'Minor (reclaiming a frame) page faults',
        },
        'voluntary_switch': {
            'desc': 'Voluntary context switches',
        },
        'involuntary_switch': {
            'desc': 'Involuntary context switches',
        },
    }
    for column, column_details in columns.items():
        create_graph(session_results, column=column, column_desc=column_details['desc'], per_value=per_value, desc=desc)
