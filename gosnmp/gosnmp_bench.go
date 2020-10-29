package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"time"

	g "github.com/soniah/gosnmp"
	_ "crypto/sha1"
)

func main() {
	if len(os.Args) != 8 {
		log.Fatalf("8 args expected, %v received", len(os.Args))
	}
	host := os.Args[1]
	port, err := strconv.Atoi(os.Args[2])
	if err != nil {
		log.Fatalf("port arg err: %v", err)
	}
	oid_batch_size, err := strconv.Atoi(os.Args[3])
	if err != nil {
		log.Fatalf("port arg err: %v", err)
	}
	sessions_num, err := strconv.Atoi(os.Args[4])
	if err != nil {
		log.Fatalf("sessions arg err: %v", err)
	}
	rounds, err := strconv.Atoi(os.Args[5])
	if err != nil {
		log.Fatalf("rounds arg err: %v", err)
	}
	print_results := os.Args[6]
	if err != nil {
		log.Fatalf("print_results arg err: %v", err)
	}
	snmp_version := os.Args[7]
	if err != nil {
		log.Fatalf("version arg err: %v", err)
	}

	var sessions []g.GoSNMP

	for i := 0; i < sessions_num; i++ {
		var session g.GoSNMP
		if snmp_version == "3" {
			session = g.GoSNMP{
				Target: host,
				Port:               uint16(port),
				ContextName:        "public",
				Timeout:            time.Duration(2) * time.Second,
				Retries:            3,
				ExponentialTimeout: true,
				MaxOids:            100,
				Version:            g.Version3,
				SecurityModel: 		g.UserSecurityModel,
				MsgFlags:      		g.AuthPriv,
				SecurityParameters: &g.UsmSecurityParameters{
					UserName: "datadogSHAAES",
					AuthenticationProtocol:   g.SHA,
					AuthenticationPassphrase: "doggiepass",
					PrivacyProtocol:          g.AES,
					PrivacyPassphrase:        "doggiePRIVkey",
				},
			}
		} else {
			session = g.GoSNMP{
				Target: host,
				Port:               uint16(port),
				Community:          "public",
				Version:            g.Version2c,
				Timeout:            time.Duration(2) * time.Second,
				Retries:            3,
				ExponentialTimeout: true,
				MaxOids:            100,
			}
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
		for j := 0; j < rounds; j++ {
			result, err2 := sessions[i].Get(oids)
			if err2 != nil {
				log.Fatalf("Get() err: %v", err2)
			}
			if print_results == "true" {
		    	results = append(results, result)
			}
		}
	}

	elapsed := time.Since(start)

	for i, result := range results {
		fmt.Printf("Session: %d\n", i)

		for j, variable := range result.Variables {
			fmt.Printf("%d: oid: %s ", j, variable.Name)
			switch variable.Type {
			case g.OctetString:
				fmt.Printf("string: %s\n", string(variable.Value.([]byte)))
			default:
				fmt.Printf("number: %d\n", g.ToBigInt(variable.Value))
			}
		}
	}

	fmt.Printf("gosnmp duration: %.2f ms\n", float32(elapsed) / 1000000)
}
