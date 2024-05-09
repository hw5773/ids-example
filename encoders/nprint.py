import sys
import logging
from encoders.encoder import Encoder
import dpkt

class Nprint(Encoder):
    def __init__(self, name):
        super().__init__(name)

    def encode(self, packet):

        code = []
        data = None
        tcp = [-1 for _ in range(8 * 20)]
        udp = [-1 for _ in range(8 * 8)]
        icmp = [-1 for _ in range(8 * 8)]

        if isinstance(packet.network.data, dpkt.udp.UDP):
            data = bytes(packet.network.data)[:8]
            udp = list(''.join(list(map(lambda b : format(b, '08b').split('b')[-1], data))))
            udp = list(map(int, udp))

        elif isinstance(packet.network.data, dpkt.tcp.TCP):
            data = bytes(packet.network.data)[:20]
            tcp = list(''.join(list(map(lambda b : format(b, '08b').split('b')[-1], data))))
            tcp = list(map(int, tcp))

        elif isinstance(packet.network.data, dpkt.icmp.ICMP):
            data = bytes(packet.network.data)[:8]
            icmp = list(''.join(list(map(lambda b : format(b, '08b').split('b')[-1], data))))
            icmp = list(map(int, icmp))

        nprint = tcp + udp + icmp

        #with open('nprint.txt', 'a') as file:
        #    if packet.network.p == 1:
        #        file.write('== ICMP ==================================================================\n\n')
        #    elif packet.network.p == 6:
        #        file.write('== TCP ==================================================================\n\n')
        #    elif packet.network.p == 17:
        #        file.write('== UDP ==================================================================\n\n')

        #    file.write('network : \n{}\n\n'.format(packet.network))
        #    file.write('network repr : \n{}\n\n'.format(repr(packet.network)))
        #    file.write('network data : \n{}\n\n'.format(packet.network.data))
        #    file.write('data : {}\n\n'.format(data))
        #    file.write('tcp : {}\n\n'.format(tcp))
        #    file.write('udp : {}\n\n'.format(udp))
        #    file.write('icmp : {}\n\n'.format(icmp))
        #    file.write('nprint : {}\n\n'.format(nprint))

        logging.debug('{}: {}'.format(self.get_name(), code))
        packet.set_code(self.get_name(), code)
