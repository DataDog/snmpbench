import sys

import netsnmp

host = sys.argv[1]
port = int(sys.argv[2])  # default port is 1161 and cannot be be changed
count = int(sys.argv[3])

import time


oids = []
for i in range(1, count+1):
    oids.append(netsnmp.Varbind('.1.3.6.1.2.1.25.6.3.1.1', i))

sess = netsnmp.Session(Version=2,
                       DestHost="{}:{}".format(host, port),
                       Community='public')

vars = netsnmp.VarList(*oids)

start = time.time()
vals = sess.get(vars)
end = time.time()

# for val in vals:
#     print("val", val, type(val))
for i, oid in enumerate(oids):
    print("oid=%s, val=%s" % (oid.tag, vals[i]))

print("netsnmp duration: {:.2f} ms".format((end - start) * 1000))
