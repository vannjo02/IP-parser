#!/usr/bin/python3
#encoding: UTF-8

from DNSclient import*

if __name__ == "__main__":
    d = DNSClient()
    domain = input("Enter domain name\n")
    rec_type = input("Enter record type (A, AAAA)\n")
    resp = input("Enter domain name server address? (y or n) \n")
    if resp == 'y':
        server = input("Enter DNS server: \n")
    else: 
        server = "8.8.8.8"
    ans = d.resolve(domain, rec_type, server)
    print("Domain: ", domain)
    print("Record type: ", rec_type)
    print("DNS server: ", server)
    print("IP Address: ", ans)
