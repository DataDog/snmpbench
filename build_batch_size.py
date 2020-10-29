from utils import get_results, create_all_graphs

print("Run Batch Size")


def build_per_batch_size(snmp_version):
    results = {}
    base_options = {
        'round': 10,
        'session': 10,
        'snmp_version': snmp_version,
    }
    for i in [5, 10, 15, 20, 50, 100]:
        kwargs = base_options.copy()
        kwargs.update({
            'oid_batch_size': i,
        })
        print("Run for params: {}".format(kwargs))
        results[i] = get_results(**kwargs)

    create_all_graphs(results, per_value='batch_size', desc="params: {}".format(base_options))


for snmp_version in ['2', '3']:
    build_per_batch_size(snmp_version)
