import json
from collections import defaultdict
from utils import get_results


print("Run build_max_rss_per_rounds")


def build_max_rss_per_rounds():
    import matplotlib.pyplot as plt

    session_results = {}
    for i in [1, 10, 20, 50, 100, 150, 200]:
        kwargs = {
            'oid_batch_size': 50,
            'rounds': i,
            'sessions': 10,
        }
        print("Run for params: {}".format(kwargs))
        session_results[i] = get_results(**kwargs)

    sessions = session_results.keys()
    per_lib = defaultdict(list)
    for _, results in session_results.items():
        for result in results['results']:
            per_lib[result['name']].append(result['max_rss'])
    for lib, values in per_lib.items():
        plt.plot(sessions, values, label=lib)
    plt.xlabel('Rounds')
    plt.ylabel('Max RSS (KBytes)')
    plt.legend()
    plt.savefig('docs/generated_data/max_rss_per_rounds.png', bbox_inches='tight')
    with open('docs/generated_data/max_rss_per_rounds.json', 'w') as f:
        f.write(json.dumps(session_results, indent=4, sort_keys=True))


build_max_rss_per_rounds()
