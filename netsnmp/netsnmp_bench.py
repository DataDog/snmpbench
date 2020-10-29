import sys
import time
import netsnmp


host = sys.argv[1]
port = int(sys.argv[2])  # default port is 1161 and cannot be be changed
oid_batch_size = int(sys.argv[3])
sessions_num = int(sys.argv[4])
rounds = int(sys.argv[5])
print_results = sys.argv[6]
snmp_version = sys.argv[7]

oids = []
for i in range(1, oid_batch_size + 1):
    oids.append(netsnmp.Varbind('.1.3.6.1.2.1.25.6.3.1.1', i))

sessions = []
for _ in range(sessions_num):
    if snmp_version == '3':
        session = netsnmp.Session(Version=3,
            DestHost="{}:{}".format(host, port),
            SecLevel='authPriv',
            SecName='datadogSHADES',
            AuthProto='SHA',
            AuthPass='doggiepass',
            PrivProto='DES',
            PrivPass='doggiePRIVkey',
            Context='public',
        )
    else:
        session = netsnmp.Session(Version=2,
            DestHost="{}:{}".format(host, port),
            Community='public',
        )
    sessions.append(session)

vars = netsnmp.VarList(*oids)
session_vals = []

start = time.time()
for sess in sessions:
    for _ in range(rounds):
        res = sess.get(vars)
        if print_results == 'true':
            session_vals.append(res)
end = time.time()

for i, vals in enumerate(session_vals):
    print("Session {}".format(i))
    for j, oid in enumerate(oids):
        print("oid=%s, val=%s" % (oid.tag, vals[j]))

print("netsnmp duration: {:.2f} ms".format((end - start) * 1000))
