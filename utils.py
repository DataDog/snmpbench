import json
import subprocess
import tempfile


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
