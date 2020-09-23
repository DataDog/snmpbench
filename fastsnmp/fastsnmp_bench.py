import sys

host = sys.argv[1]
port = int(sys.argv[2])  # default port is 1161 and cannot be be changed
count = int(sys.argv[3])

import time


oids = []
for i in range(1, count+1):
    oids.append('1.3.6.1.2.1.25.6.3.1.1.{}'.format(i))

start = time.time()

from fastsnmp import snmp_poller

hosts = (host,)

community = "public"
snmp_data = snmp_poller.poller(hosts, [list(oids)], community, msg_type='Get')

snmp_data = list(snmp_data)
end = time.time()

for d in snmp_data:
    print ("host=%s oid=%s value=%s" % (d[0], d[1], d[3]))

print("duration: {:.2f} ms".format((end - start) * 1000))
