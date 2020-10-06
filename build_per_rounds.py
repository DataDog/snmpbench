from utils import get_results, create_all_graphs

print("Run Rounds")


def build_per_rounds():
    results = {}
    for i in [1, 10, 20, 50, 100, 150, 200]:
        kwargs = {
            'oid_batch_size': 50,
            'rounds': i,
            'sessions': 1,
        }
        print("Run for params: {}".format(kwargs))
        results[i] = get_results(**kwargs)

    create_all_graphs(results, per_value='rounds')


build_per_rounds()
