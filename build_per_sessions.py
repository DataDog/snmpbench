from utils import get_results, create_all_graphs

print("Run build_max_rss_per_sessions")


def build_max_rss_per_sessions():
    results = {}
    for i in [1, 10, 20, 50, 100, 150, 200]:
        kwargs = {
            'oid_batch_size': 50,
            'rounds': 1,
            'sessions': i,
        }
        print("Run for params: {}".format(kwargs))
        results[i] = get_results(**kwargs)

    create_all_graphs(results, per_value='sessions')


build_max_rss_per_sessions()
