from utils import get_results, create_all_graphs

print("Run Rounds")


def build_per_round():
    results = {}
    base_options = {
        'oid_batch_size': 50,
        'session': 1,
    }
    for i in [1, 10, 20, 50, 100, 150, 200, 300, 400]:
        kwargs = base_options.copy()
        kwargs.update({
            'round': i,
        })
        print("Run for params: {}".format(kwargs))
        results[i] = get_results(**kwargs)

    create_all_graphs(results, per_value='round', desc="params: {}".format(base_options))


build_per_round()
