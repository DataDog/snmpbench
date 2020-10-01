import sys
from pysnmp.hlapi import *

host = sys.argv[1]
port = int(sys.argv[2])
oid_batch_size = int(sys.argv[3])

import time


oids = []
for i in range(1, oid_batch_size + 1):
    oids.append(ObjectType(ObjectIdentity('1.3.6.1.2.1.25.6.3.1.1.{}'.format(i))))

start = time.time()

iterator = getCmd(SnmpEngine(),
                  CommunityData('public'),
                  UdpTransportTarget((host, port)),
                  ContextData(),
                  *oids
            )


errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

end = time.time()

if errorIndication:  # SNMP engine errors
    print(errorIndication)
else:
    if errorStatus:  # SNMP agent errors
        print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex)-1] if errorIndex else '?'))
    else:
        for varBind in varBinds:  # SNMP response contents
            print(' = '.join([x.prettyPrint() for x in varBind]))


print("pysnmp duration: {:.2f} ms".format((end - start) * 1000))
