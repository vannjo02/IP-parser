#!/usr/bin/python3
#encoding: UTF-8

from socket import *
from random import randint
import ipaddress

PORT = 53

class DNSClient:
    def __init__(self):
        self.msg_qry = bytearray()
        self.trans_id = randint(0, 65535)
    
    def format_query(self, query_domain, query_type):
        flags = 0x100 # default
        questions = 1 # default
        rr_ans =0 # default
        rr_auth = 0 # default
        rr_add = 0 # default
        q_name_lst = query_domain.split('.')
        try:
            if query_type == "A":
                q_type = 1
            elif query_type == "AAAA":
                q_type = 28
        
        except:
            raise Exception("Unknown query type")
        q_class = 1 # default
        
        # Splitting values into 2 bytes and building the array (request)
        self.msg_qry.append((self.trans_id & 0xff00) >> 8)
        self.msg_qry.append(self.trans_id & 0x00ff)
        self.msg_qry.append((flags & 0xff00) >> 8)
        self.msg_qry.append(flags & 0x00ff)
        self.msg_qry.append((questions & 0xff00) >> 8)
        self.msg_qry.append(questions & 0x00ff)
        self.msg_qry.append((rr_ans & 0xff00) >> 8)
        self.msg_qry.append(rr_ans & 0x00ff)
        self.msg_qry.append((rr_auth & 0xff00) >> 8)
        self.msg_qry.append(rr_auth & 0x00ff)
        self.msg_qry.append((rr_add & 0xff00) >> 8)
        self.msg_qry.append(rr_add & 0x00ff)
        for d in q_name_lst:
            self.msg_qry.append(len(d))
            for c in d:
                self.msg_qry.append(ord(c))
            # TODO: Append domain name in the following format: length name for each subdomain
            # Check project references (resources) for details 

        self.msg_qry.append(0) # terminate domain name
        self.msg_qry.append((q_type & 0xff00) >> 8)
        self.msg_qry.append(q_type & 0x00ff)
        self.msg_qry.append((q_class & 0xff00) >> 8)
        self.msg_qry.append(q_class & 0x00ff)
    
    def parse_answer(self, msg_resp):
        # TODO: Write a parser for A, and AAAA records
        
        
        array = bytearray()
        for item in msg_resp:
            array.append(item)
                        
            
        length = msg_resp[msg_resp.index(0xc0) + 11]
        addr = msg_resp[len(msg_resp)-length:]
        if len(addr) == 16:
            ip = ipaddress.IPv6Address(addr)
        else: 
            ip = ipaddress.IPv4Address(addr)
        
        return ip
    
    def resolve(self, query_domain, query_type, server):
        self.format_query(query_domain, query_type)
        client_sckt = socket(AF_INET, SOCK_DGRAM)
        client_sckt.sendto(self.msg_qry, (server,PORT))
        (msg_resp, server_addr) = client_sckt.recvfrom(2048)
        client_sckt.close()
        
        # TODO: Send the formatted query to the server and receive the response

        return self.parse_answer(msg_resp)
        
    # Split a value into 2 bytes
    def val_2_byte(self, value):
        byte_1 = (value & 0xff00) >> 8
        byte_2 = value & 0x00ff
        
        return [byte_1, byte_2]
    # Merge 2 bytes into a value
    def byte_2_val(self, bytes_lst):
        value = 0
        for b in bytes_lst:
            value = (value << 8) + b
        
        return value