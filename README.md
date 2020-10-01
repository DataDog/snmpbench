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
          :   duration    max_rss
gosnmp    :      22.10       3564
netsnmp   :      26.09      12148
pysnmp    :     182.08      31096
```
