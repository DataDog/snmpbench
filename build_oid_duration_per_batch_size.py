import json
from collections import defaultdict
from utils import get_results


print("Run oid_duration_per_batch_size")


def build_oid_duration_per_batch_size():
    import matplotlib.pyplot as plt

    session_results = {}
    for i in [5, 10, 15, 20, 50, 100]:
        kwargs = {
            'oid_batch_size': i,
            'rounds': 10,
            'sessions': 10,
        }
        print("Run for params: {}".format(kwargs))
        session_results[i] = get_results(**kwargs)

    sessions = session_results.keys()
    per_lib = defaultdict(list)
    for _, results in session_results.items():
        for result in results['results']:
            per_lib[result['name']].append(result['duration_per_oid'])
    for lib, values in per_lib.items():
        plt.plot(sessions, values, label=lib)
    plt.xlabel('Batch Size')
    plt.ylabel('Duration Per OID (ms)')
    plt.legend()
    plt.savefig('docs/generated_data/oid_duration_per_batch_size.png', bbox_inches='tight')
    with open('docs/generated_data/oid_duration_per_batch_size.json', 'w') as f:
        f.write(json.dumps(session_results, indent=4, sort_keys=True))


build_oid_duration_per_batch_size()
