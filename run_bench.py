import subprocess

hostname = 'localhost'
port = 1161
number = 100

LIBS = {
    'gosnmp': {
        'setup': ['go', 'build', '-o', 'gosnmp/gosnmp_bench', 'gosnmp/gosnmp_bench.go'],
        'exec': ['./gosnmp/gosnmp_bench', hostname, str(port), str(number)]
    },
    'netsnmp': {
        'exec': ['python', 'netsnmp/netsnmp_bench.py', hostname, str(port), str(number)]
    },
    'pysnmp': {
        'exec': ['python', 'pysnmp/pysnmp_bench.py', hostname, str(port), str(number)]
    }
}

for lib, config in LIBS.items():
    setup_cmd = config.get('setup')
    exec_cmd = config['exec']
    if setup_cmd:
        setup_res = subprocess.check_output(setup_cmd)

    p = subprocess.Popen(exec_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    exec_res, stderr = p.communicate()
    if stderr:
        raise Exception("stderr: {}".format(stderr.strip()))

    exec_res = exec_res.decode('utf-8')
    for line in exec_res.split('\n'):
        if 'duration' in line:
            duration = line.split()[2]
            break
    else:
        raise Exception('No duration found')

    print("Duration for {:10s}: {:>8s}".format(lib, duration))
