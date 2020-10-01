
def get_configs(hostname, port, oid_batch_size):
    return {
        'gosnmp': {
            'setup': ['go', 'build', '-o', 'gosnmp/gosnmp_bench', 'gosnmp/gosnmp_bench.go'],
            'exec': ['/usr/bin/time', '-v', './gosnmp/gosnmp_bench', hostname, str(port), str(oid_batch_size)]
        },
        'netsnmp': {
            'exec': ['/usr/bin/time', '-v', 'python', 'netsnmp/netsnmp_bench.py', hostname, str(port),
                     str(oid_batch_size)]
        },
        'pysnmp': {
            'exec': ['/usr/bin/time', '-v', 'python', 'pysnmp/pysnmp_bench.py', hostname, str(port),
                     str(oid_batch_size)]
        }
    }
