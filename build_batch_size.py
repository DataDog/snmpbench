from utils import get_results, create_all_graphs

print("Run Batch Size")


def build_per_batch_size():
    results = {}
    base_options = {
        'round': 10,
        'session': 10,
    }
    for i in [5, 10, 15, 20, 50, 100]:
        kwargs = base_options.copy()
        kwargs.update({
            'oid_batch_size': i,
        })
        print("Run for params: {}".format(kwargs))
        results[i] = get_results(**kwargs)

    create_all_graphs(results, per_value='batch_size', title="Options: {}".format(base_options))


build_per_batch_size()
