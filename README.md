# snmpbench

Work In Progress

## Libs to benchmark

Python
- [pysnmp](https://github.com/etingof/pysnmp)
- [python3-netsnmp (bindings)](https://github.com/bluecmd/python3-netsnmp)
- custom lib without MIB support?

Go
- [gosnmp](https://github.com/soniah/gosnmp)
- netsnmp using CGO
- custom lib without MIB support?


## Extra

Other interesting libs

Python
- [fastsnmp](https://github.com/gescheit/fastsnmp)
- [easysnmp](https://github.com/fgimian/easysnmp)


## [Draft] bench

```
$ python run_bench.py localhost 1161 --oid-batch-size 50 --sessions 100 --rounds 10
SNMP Benchmark
oid_batch_size: 50
sessions: 100
rounds: 10
print_results: false
               duration(ms)     duration_per_oid      max_rss(kbytes)         rss_per_sess
gosnmp    :        11073.91             0.221478                15548                  155
netsnmp   :        11171.24             0.223425                12080                  120
pysnmp    :        17923.49             0.358470               126680                 1266
```

