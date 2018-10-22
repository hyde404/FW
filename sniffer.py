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
    s.bind(("YOUR_INTERFACE_IP",0))
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

    eth = unpack.eth_header(packet[0:14])
    iph = unpack.ip_header(packet[14:34])


    if iph.get("Protocol") == 6 :
        tcph = unpack.tcp_header(packet[34:54])
        compteur.add_tcp(tcph.get("Destination Port"), iph.get("Source Address"))
    elif iph.get("Protocol") == 17 :
        udph = unpack.udp_header(packet[34:42])
        compteur.add_udp(udph.get("Destination Port"), iph.get("Source Address"))
    elif iph.get("Protocol") == 1 :
        icmph = unpack.icmp_header(packet[34:42])
        compteur.add_icmp(iph.get("Source Address"))

    if interrupted:
        print("Ha ! (cf: D.Brognard)")
        break

# TODO : BLBLB sort tableau et print et fichier et sushi