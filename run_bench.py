import subprocess
import tempfile

hostname = 'localhost'
port = 1161
number = 100

LIBS = {
    'gosnmp': {
        'setup': ['go', 'build', '-o', 'gosnmp/gosnmp_bench', 'gosnmp/gosnmp_bench.go'],
        'exec': ['/usr/bin/time', '-v', './gosnmp/gosnmp_bench', hostname, str(port), str(number)]
    },
    'netsnmp': {
        'exec': ['/usr/bin/time', '-v', 'python', 'netsnmp/netsnmp_bench.py', hostname, str(port), str(number)]
    },
    'pysnmp': {
        'exec': ['/usr/bin/time', '-v', 'python', 'pysnmp/pysnmp_bench.py', hostname, str(port), str(number)]
    }
}


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


for lib, config in LIBS.items():
    setup_cmd = config.get('setup')
    exec_cmd = config['exec']
    if setup_cmd:
        setup_res, stderr, code = subprocess_output(exec_cmd)
        if code != 0:
            raise Exception("stderr: {}".format(stderr.strip()))

    exec_res, stderr, code = subprocess_output(exec_cmd)
    if code != 0:
        raise Exception("stderr: {}".format(stderr.strip()))

    exec_res = exec_res.decode('utf-8')
    for line in exec_res.split('\n'):
        if 'duration' in line:
            duration = line.split()[2]
            break
    else:
        raise Exception('No duration found')

    print("Duration for {:10s}: {:>8s}".format(lib, duration))
