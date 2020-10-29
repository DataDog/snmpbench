import sys
import time

from pysnmp import hlapi
from pysnmp.hlapi import *
from pysnmp.entity import engine
from pysnmp.entity.rfc3413 import cmdgen
from pysnmp.hlapi.asyncore.cmdgen import lcd, UdpTransportTarget, CommunityData, ContextData


host = sys.argv[1]
port = int(sys.argv[2])
oid_batch_size = int(sys.argv[3])
sessions_num = int(sys.argv[4])
rounds = int(sys.argv[5])
print_results = sys.argv[6]
snmp_version = sys.argv[7]


def register_device_target(ip, port, timeout, retries, engine, auth_data, context_data):
    # type: (str, int, float, int, SnmpEngine, Any, ContextData) -> str
    transport = UdpTransportTarget((ip, port), timeout=timeout, retries=retries)
    target, _ = lcd.configure(engine, auth_data, transport, context_data.contextName)
    return target


def callback_fn(snmpEngine, sendRequestHandle, errorIndication,
                errorStatus, errorIndex, varBinds, cbCtx):
    if errorIndication:
        print("ERROR errorIndication:", errorIndication)
        exit(1)
    elif errorStatus:
        print('ERROR %s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        exit(1)
    else:
        if print_results == 'true':
            for oid, val in varBinds:
                print('%s : print=`%s` type=`%s`' % (oid.prettyPrint(), val.prettyPrint(), type(val)))


oids = []
for i in range(1, oid_batch_size + 1):
    oids.append(('1.3.6.1.2.1.25.6.3.1.1.{}'.format(i), None))

sessions = []


if snmp_version == '3':
    context_name = 'public'
else:
    context_name = ''

for _ in range(sessions_num):
    if snmp_version == '3':
        auth_data = UsmUserData('datadogSHAAES', 'doggiepass', 'doggiePRIVkey', hlapi.usmHMACSHAAuthProtocol,
                                hlapi.usmAesCfb128Protocol)
        context_data = ContextData(contextEngineId=None, contextName=context_name)
    else:
        auth_data = CommunityData('public', mpModel=1)
        context_data = ContextData()
    snmpEngine = engine.SnmpEngine()
    target = register_device_target(
        host,
        port,
        timeout=3,
        retries=3,
        engine=snmpEngine,
        auth_data=auth_data,
        context_data=context_data,
    )
    sessions.append((snmpEngine, target))


start = time.time()

for snmpEngine, target in sessions:
    for _ in range(rounds):
        cmdgen.GetCommandGenerator().sendVarBinds(
            snmpEngine,
            target,
            None, context_name,  # contextEngineId, contextName
            oids,
            callback_fn
        )
        snmpEngine.transportDispatcher.runDispatcher()

end = time.time()

print("pysnmp duration: {:.2f} ms".format((end - start) * 1000))
