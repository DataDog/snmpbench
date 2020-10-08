from utils import get_results, create_all_graphs

print("Run Batch Size")


def build_per_batch_size():
    results = {}
    for i in [5, 10, 15, 20, 50, 100]:
        kwargs = {
            'oid_batch_size': i,
            'round': 10,
            'session': 10,
        }
        print("Run for params: {}".format(kwargs))
        results[i] = get_results(**kwargs)

    create_all_graphs(results, per_value='batch_size')


build_per_batch_size()
