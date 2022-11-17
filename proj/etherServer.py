#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import socket
import ethernetTools as et

if __name__ == "__main__":
    sck = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(et.ETH_P_ALL))  #creates RAW ethernet socket
    sck.bind(("eth0", 0))     #Binding ethernet interface to the socket
    
    #eth0 - default name of the ethernet interface in UNIX
    my_addr = et.get_self_addr(sck, 'eth0')
    #prints ethernet address in human-readable format
    print('Ethernet address:', et.bytes_ether_addr_to_string(my_addr))

    my_ip=et.get_self_ip_addr(sck, 'eth0')
    print('IP: ', et.bytes_ip_addr_to_string(my_ip))

    while True:           
        #Keeps waiting for ethernet frames and prints them
        print("Waiting for an ethernet frame...")
        #receives an ethenet frame
        recv_frame = sck.recv(et.MAX_FRAME_SIZE)
    
        #extracts content of the frame
        my_addr_in_frame, sender_addr, _, msg = et.extract_frame(recv_frame)

        if(msg == et.bytes_ip_addr_to_string(my_ip)):  
            print("Ethernet frame received!")
            msgrep="Hi, I'm the Server you are looking for!"
            frame = et.build_frame(sender_addr, my_addr, msgrep)
            sck.send(frame)
        print()
    
    sck.close()
