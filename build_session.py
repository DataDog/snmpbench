from utils import get_results, create_all_graphs

print("Run build_max_rss_per_sessions")


def build_per_session():
    results = {}
    base_options = {
        'oid_batch_size': 50,
        'round': 1,
    }
    for i in [1, 10, 20, 50, 100, 150, 200, 300, 400]:
        kwargs = base_options.copy()
        kwargs.update({
            'session': i,
        })
        print("Run for params: {}".format(kwargs))
        results[i] = get_results(**kwargs)

    create_all_graphs(results, per_value='session', title="Options: {}".format(base_options))


build_per_session()
