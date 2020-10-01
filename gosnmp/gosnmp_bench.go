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
	if len(os.Args) != 4 {
		log.Fatalf("4 args expected, %v received", len(os.Args))
	}
	host := os.Args[1] // first command line parameter, ...
	port, err := strconv.Atoi(os.Args[2]) // first command line parameter, ...
	if err != nil {
		log.Fatalf("port arg err: %v", err)
	}
	count, err := strconv.Atoi(os.Args[3]) // first command line parameter, ...
	if err != nil {
		log.Fatalf("port arg err: %v", err)
	}

	// Default is a pointer to a GoSNMP struct that contains sensible defaults
	// eg port 161, community public, etc
	g.Default.Target = host
	g.Default.Port = uint16(port)
	g.Default.MaxOids = 100
	err = g.Default.Connect()
	if err != nil {
		log.Fatalf("Connect() err: %v", err)
	}
	defer g.Default.Conn.Close()

	start := time.Now()

	oids := []string{}
	for i := 1; i <= count; i++ {
		oids = append(oids, "1.3.6.1.2.1.25.6.3.1.1." + strconv.Itoa(i))
	}
	result, err2 := g.Default.Get(oids) // Get() accepts up to g.MAX_OIDS

	elapsed := time.Since(start)



	if err2 != nil {
		log.Fatalf("Get() err: %v", err2)
	}

	for i, variable := range result.Variables {
		fmt.Printf("%d: oid: %s ", i, variable.Name)

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

	fmt.Printf("gosnmp duration: %.2f ms\n", float32(elapsed) / 1000000)
}