#!usr/bin/python
import socket
import signal
import os

import pye
import compteur

# Variables
local_ip = socket.gethostbyname(socket.gethostname())
interrupted = False

# Fonctions
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

if os.name == "nt":
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    s.bind((local_ip,0))
    print("Monitoring de l\' adresse %s" % local_ip)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL,1)
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
else:
    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))

# Handler
signal.signal(signal.SIGINT, signal_handler)


unpack = pye.unpack()
compteur = compteur.cpt()

# Boucle de gestion des paquets
while True:
    try:
        packet = s.recvfrom(65565)[0]
    except socket.error:
        break

    eth_length=20
    #eth = unpack.eth_header(packet[0:14])
    #print(eth)
    #iph = unpack.ip_header(packet[14:34])
    iph = unpack.ip_header(packet[:eth_length])
    print(iph)
    #tph = unpack.tcp_header(packet[34:54])
    #print(tph)

    if iph.get("Protocol") == 6 :
        tcph = unpack.tcp_header(packet[eth_length:eth_length+20])
        print(tcph)
        # compteur.add_tcp(tcph.get("Destination Port"), iph.get("Source Address"))
        print("version 6")
    elif iph.get("Protocol") == 17 :
        udph = unpack.udp_header(packet[eth_length:eth_length+8])
        print(udph)
        # compteur.add_udp(udph.get("Destination Port"), iph.get("Source Address"))
        print("version 17")
    elif iph.get("Protocol") == 1 :
        icmph = unpack.icmp_header(packet[eth_length:eth_length+4])
        print(icmph)
        # compteur.add_icmp(iph.get("Source Address"))
        print("version 1")
    else :
        print("ne matche rien")

    if interrupted:
        print("Terminated")
        break

# TODO : BLBLB sort tableau et print et fichier