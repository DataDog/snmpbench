import sys
import time

from pysnmp.hlapi import *
from pysnmp.entity import engine
from pysnmp.entity.rfc3413 import cmdgen
from pysnmp.hlapi.asyncore.cmdgen import lcd, UdpTransportTarget, CommunityData, ContextData

host = sys.argv[1]
port = int(sys.argv[2])
oid_batch_size = int(sys.argv[3])
sessions_num = int(sys.argv[4])

oids = []
for i in range(1, oid_batch_size + 1):
    oids.append(('1.3.6.1.2.1.25.6.3.1.1.{}'.format(i), None))

sessions = []

def register_device_target(ip, port, timeout, retries, engine, auth_data, context_data):
    # type: (str, int, float, int, SnmpEngine, Any, ContextData) -> str
    transport = UdpTransportTarget((ip, port), timeout=timeout, retries=retries)
    target, _ = lcd.configure(engine, auth_data, transport, context_data.contextName)
    return target

for _ in range(sessions_num):
    snmpEngine = engine.SnmpEngine()
    target = register_device_target(
        host,
        port,
        timeout=3,
        retries=3,
        engine=snmpEngine,
        auth_data=CommunityData('public', mpModel=1),
        context_data=ContextData(),
    )
    sessions.append((snmpEngine, target))

def cbFun(snmpEngine, sendRequestHandle, errorIndication,
          errorStatus, errorIndex, varBinds, cbCtx):
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for oid, val in varBinds:
            print('%s : print=`%s` type=`%s`' % (oid.prettyPrint(), val.prettyPrint(), type(val)))


start = time.time()

for snmpEngine, target in sessions:
    cmdgen.GetCommandGenerator().sendVarBinds(
        snmpEngine,
        target,
        None, '',  # contextEngineId, contextName
        oids,
        cbFun
    )
    snmpEngine.transportDispatcher.runDispatcher()

end = time.time()

print("pysnmp duration: {:.2f} ms".format((end - start) * 1000))
