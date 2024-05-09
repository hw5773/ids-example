import argparse
import os
import logging
import time
import sys
import dpkt
import socket
sys.path.append("..")
from scapy.all import rdpcap
from definitions.packet import Packet
from definitions.packet_header import PacketHeader

class PacketCapturer:
    def __init__(self, core, name, conf):
        self.core = core
        self.name = name
        self.config = conf

        self.packets = {}
        pname = conf.get("training_packets", None)
        lname = conf.get("training_label", None)
        self.packets["training"] = init_packets(pname, lname)
        pname = conf.get("testing_packets", None)
        lname = conf.get("testing_label", None)
        self.packets["testing"] = init_packets(pname, lname)

    def get_packets(self, phase):
        return self.packets[phase]

def init_packets(pname, lname):
    if not pname or not lname:
        logging.error("the pcap file or the label file is not correctly set")
        logging.error("please try again with the correct configuration file")
        sys.exit(1)

    if not os.path.exists(pname):
        logging.error("the pcap file ({}) does not exist".format(pname))
        logging.error("please try again with the correct configuration file")
        sys.exit(1)

    if not os.path.exists(lname):
        logging.error("the label file ({}) does not exist".format(lname))
        logging.error("please try again with the correct configuration file")
        sys.exit(1)

    packets = rdpcap(pname)
    labels = parse_label(lname)
    logging.debug("# of packets in {}: {}".format(pname, len(packets)))
    logging.debug("# of labels in {}: {}".format(lname, len(labels)))

    num = 0
    for packet in packets:
        pbytes = bytes(packet)
        pkt = parse_packet(packet.time, pbytes)
        num += 1

        if pkt:
            try:
                pkt.set_label(labels[num])
            except:
                pkt.set_label(0)

    return packets

def parse_packet(ts, packet):
    eth = dpkt.ethernet.Ethernet(packet)

    if not isinstance(eth.data, dpkt.ip.IP):
        logging.error("Non IP packet type not supported: {}".format(eth.data.__class__.__name__))
        return None

    length = len(packet)
    ip = eth.data
    df = bool(ip.off & dpkt.ip.IP_DF)
    mf = bool(ip.off & dpkt.ip.IP_MF)
    offset = bool(ip.off & dpkt.ip.IP_OFFMASK)

    protocol = ip.p
    trans = None

    if protocol == 1:
        logging.debug("ICMP: {} -> {}".format(inet_to_str(ip.src), inet_to_str(ip.dst)))

    elif protocol == 6:
        if not isinstance(ip.data, dpkt.tcp.TCP):
            logging.error("TCP error")
            return None
        tcp = ip.data
        sport = tcp.sport
        dport = tcp.dport
        logging.debug("TCP/IP: {}:{} -> {}:{} (len={})".format(inet_to_str(ip.src), sport, inet_to_str(ip.dst), dport, ip.len))
        trans = tcp
        key = "{}:{}:{}:{}".format(inet_to_str(ip.src), sport, inet_to_str(ip.dst), dport)

    elif protocol == 17:
        if not isinstance(ip.data, dpkt.udp.UDP):
            logging.error("UDP error")
            return None
        udp = ip.data
        sport = udp.sport
        dport = udp.dport
        logging.debug("UDP/IP: {}:{} -> {}:{} (len={})".format(inet_to_str(ip.src), sport, inet_to_str(ip.dst), dport, ip.len))
        trans = udp
        key = "{}:{}:{}:{}".format(inet_to_str(ip.src), sport, inet_to_str(ip.dst), dport)

    else:
        logging.error("Not supported protocol")
        return None

    return Packet(ts, eth, ip, trans, length)

def parse_label(lname):
    ret = {}
    with open(lname, "r") as f:
        for line in f:
            tmp = line.strip().split(",")
            ret[int(tmp[0])] = int(tmp[-1])
    return ret

def inet_to_str(addr):
    try:
        return socket.inet_ntop(socket.AF_INET, addr)
    except:
        return socket.inet_ntop(socket.AF_INET6, addr)

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Configuration file", type=str, default="ids.conf")
    parser.add_argument("-l", "--log", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")

    args = parser.parse_args()
    return args

def main():
    args = command_line_args()

    logging.basicConfig(level=args.log)
    signature_detector = PacketCapturer(None, args.config, None)

if __name__ == "__main__":
    main()
