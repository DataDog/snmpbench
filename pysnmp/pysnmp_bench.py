import sys
from pysnmp.hlapi import *

host = sys.argv[1]
port = int(sys.argv[2])

import time

start = time.time()

oid = ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))

iterator = getCmd(SnmpEngine(),
                  CommunityData('public'),
                  UdpTransportTarget((host, port)),
                  ContextData(),
                  *([oid] * 10)
            )


errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:  # SNMP engine errors
    print(errorIndication)
else:
    if errorStatus:  # SNMP agent errors
        print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex)-1] if errorIndex else '?'))
    else:
        for varBind in varBinds:  # SNMP response contents
            print(' = '.join([x.prettyPrint() for x in varBind]))

end = time.time()
print(end - start)
