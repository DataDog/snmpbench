from collections import defaultdict
from utils import get_results


print("Run build_max_rss_per_sessions")


def build_max_rss_per_sessions():
    import matplotlib.pyplot as plt

    session_results = {}
    for i in [1, 10, 20, 50, 100, 150, 200]:
        kwargs = {
            'oid_batch_size': 50,
            'rounds': 1,
            'sessions': i,
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
    plt.xlabel('Sessions')
    plt.ylabel('Max RSS (KBytes)')
    plt.legend()
    plt.savefig('docs/generated_images/max_rss_per_sessions.png', bbox_inches='tight')


build_max_rss_per_sessions()
