# snmpbench

Benchmark for snmp libraries.

The benchmark is focused on how the library perform (Speed, Memory, CPU usage, etc) under different settings (batch size, rounds, sessions, etc).

## Benchmarked libraries

- [pysnmp](https://github.com/etingof/pysnmp)
- netsnmp using [python3-netsnmp (bindings)](https://github.com/bluecmd/python3-netsnmp)
- [gosnmp](https://github.com/soniah/gosnmp)

## Methodology

We run different **scenarios** for each library and collect measures we are interested in.

For each library, we created a program that accept various parameters ([pysnmp](pysnmp/pysnmp_bench.py), [netsnmp](netsnmp/netsnmp_bench.py), [gosnmp](gosnmp/gosnmp_bench.go))

Scenarios parameters:
- Batch size: the number of OID requested per call
- Rounds: the number of time the scenario is run
- Sessions: the number of instances of the library session/engine we create

Measurements:
- Duration per OID (ms): Average time to retrieve an OID value
- Max RSS (KBytes): maximum resident set size used by the program while running the scenario
- User time (sec): total user time taken to run the scenario 
- System Time (sec): total system time taken to run the scenario
- Elapsed Time (sec): total elapsed wall clock time taken to run the scenario

Except for `Duration per OID`, other measurements are collected using `/usr/bin/time`. 

## Results

Results can be viewed here: https://datadoghq.dev/snmpbench/

## How to run locally

**Requirements:**

```
apt install -y libsnmp-dev
pip install -r requirements.txt
go get github.com/soniah/gosnmp
```

**Run snmpsim:**

```
docker-compose -f environment/  up -d
```

**Run benchmark:**

```
python run_bench.py localhost 1161 --oid-batch-size 10 --sessions 1 --rounds 1
```

**Run scenarios:**

```
python build_batch_size.py
python build_round.py
python build_session.py
```

See results in docs/generated_data
