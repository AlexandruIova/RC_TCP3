#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import ethernetTools as et

#sys.argv[1]: ip_looking
if len(sys.argv) < 2:
    print("[ERROR]Unexpected number of arguments")
    print("Usage: python3 simpleClient.py IP_Looking_for")
    exit(0)


if __name__ == "__main__":
    #creates RAW ethernet socket
    sck = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(et.ETH_P_ALL))
    #Binding ethernet interface to the socket
    sck.bind(("eth0", 0))
    
    #eth0 - default name of the ethernet interface in UNIX
    my_addr = et.get_self_addr(sck, 'eth0')

    #argv[1]: ip searched
    print("ip looking for: ", sys.argv[1])


    target_addr = et.ether_addr_to_bytes("ff:ff:ff:ff:ff:ff")
    
    #builds frame to send
    frame = et.build_frame(target_addr, my_addr, sys.argv[1])
    sck.send(frame)
    print("Find?")
    
    while True:
        recv_frame = sck.recv(et.MAX_FRAME_SIZE)
        my_addr_in_frame, sender_addr, _, msg = et.extract_frame(recv_frame)
        if(sender_addr != my_addr):
            print("Message: ", msg)
            print("Server address: ", et.bytes_ether_addr_to_string(sender_addr))
            break


    
    sck.close()
