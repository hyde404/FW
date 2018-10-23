#!usr/bin/python
#
class cpt:

    def __init__(self):
        self.tcp = []
        self.udp = []
        self.icmp = []

    # Fonctions
    ## Ajout les informations necessaire apres reception d'un packet
    # Format des tableaux :
    # tab : [
    #        [port1, [
    #                 [compteur, ip_source1],
    #                 [compteur, ip_source2],
    #                 [compteur, ip_source3],
    #                 ...
    #                 ]
    #        ],
    #        [port2, [[compteur, ip_source1],[compteur, ip_source2],...]],
    #        ...
    #       ]

    def add_udp(self, port, s_addr):
        for i in self.udp :
            if i[0] == port :
                for j in i[1]:
                    if s_addr == j[1]:
                        j[0] += 1
                        break
                else :
                    i[1].append([1, s_addr])
                break
        else :
            self.udp.append([port,[[1, s_addr]]])

    def add_tcp(self, port, s_addr):
        for i in self.tcp :
            if i[0] == port :
                for j in i[1]:
                    if s_addr == j[1]:
                        j[0] += 1
                        break
                else :
                   i[1].append([1, s_addr])

                break
            print("result for TCP : %s" % i)
        else :
            self.tcp.append([port, [[1, s_addr]]])

    # def add_icmp(self, s_addr):
    #     for i in self.icmp:
    #         if i[1] == s_addr:
    #             i[0] += 1
    #             break
    #     else:
    #         self.icmp.append([1, source_ip])

    def print_tcp(self):
        print(self.tcp)