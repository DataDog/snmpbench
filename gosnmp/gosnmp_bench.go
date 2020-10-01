// Copyright 2012-2014 The GoSNMP Authors. All rights reserved.  Use of this
// source code is governed by a BSD-style license that can be found in the
// LICENSE file.

package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"time"

	g "github.com/soniah/gosnmp"
)

func main() {
	if len(os.Args) != 5 {
		log.Fatalf("5 args expected, %v received", len(os.Args))
	}
	host := os.Args[1] // first command line parameter, ...
	port, err := strconv.Atoi(os.Args[2]) // first command line parameter, ...
	if err != nil {
		log.Fatalf("port arg err: %v", err)
	}
	oid_batch_size, err := strconv.Atoi(os.Args[3]) // first command line parameter, ...
	if err != nil {
		log.Fatalf("port arg err: %v", err)
	}
	sessions_num, err := strconv.Atoi(os.Args[4]) // first command line parameter, ...
	if err != nil {
		log.Fatalf("sessions arg err: %v", err)
	}

	var sessions []g.GoSNMP

	for i := 0; i < sessions_num; i++ {
		session := g.GoSNMP{
			Target: host,
			Port:               uint16(port),
			Community:          "public",
			Version:            g.Version2c,
			Timeout:            time.Duration(2) * time.Second,
			Retries:            3,
			ExponentialTimeout: true,
			MaxOids:            100,
		}

		err = session.Connect()
		if err != nil {
			log.Fatalf("Connect() err: %v", err)
		}
		defer session.Conn.Close()
		sessions = append(sessions, session)
	}

	oids := []string{}
	for i := 1; i <= oid_batch_size; i++ {
		oids = append(oids, "1.3.6.1.2.1.25.6.3.1.1." + strconv.Itoa(i))
	}

	var results []*g.SnmpPacket

	start := time.Now()
	for i := 0; i < len(sessions); i++ {
		result, err2 := sessions[i].Get(oids)
		if err2 != nil {
			log.Fatalf("Get() err: %v", err2)
		}
		results = append(results, result)
	}
	elapsed := time.Since(start)

	for i, result := range results {
		fmt.Printf("Session: %d\n", i)

		for j, variable := range result.Variables {
			fmt.Printf("%d: oid: %s ", j, variable.Name)

			// the Value of each variable returned by Get() implements
			// interface{}. You could do a type switch...
			switch variable.Type {
			case g.OctetString:
				fmt.Printf("string: %s\n", string(variable.Value.([]byte)))
			default:
				// ... or often you're just interested in numeric values.
				// ToBigInt() will return the Value as a BigInt, for plugging
				// into your calculations.
				fmt.Printf("number: %d\n", g.ToBigInt(variable.Value))
			}
		}
	}

	fmt.Printf("gosnmp duration: %.2f ms\n", float32(elapsed) / 1000000)
}
