import argparse
import os
import logging
import time
import threading
import sys
import dpkt
import socket
sys.path.append("..")
from scapy.all import rdpcap
from iutils.etc import parse_config, snake_code
from modules.packet_capturer import PacketCapturer
from modules.encoder_manager import EncoderManager
from modules.model_manager import ModelManager
from modules.feature_manager import FeatureManager
from definitions.packet import Packet
from definitions.packet_header import PacketHeader

class Tester:
    def __init__(self, conf, modules, ofname):
        self.output = "{}.csv".format(ofname)
        self.modules = {}

        for module in modules:
            c = conf.get("{}".format(module), None)
            logging.info("self.modules[\"{}\"] = {}(self, \"{}\", c)".format(snake_code(module), module, module))
            exec("self.modules[\"{}\"] = {}(self, \"{}\", c)".format(snake_code(module), module, module))

        self.packets = []
        self.phase = None
        self.run()
        #self.write_result(self.packets, self.output)

    def quit(self):
        for m in self.modules:
            self.modules[m].quit()

    def run(self):
        for phase in ["training", "testing"]:
            self.phase = phase
            packets = self.modules["packet_capturer"].get_packets(phase)
            logging.info("1> phase: {}, len(packets): {}".format(phase, len(packets)))
            for packet in packets:
                self.modules["encoder_manager"].add_package(packet)
            self.modules["encoder_manager"].wait_until_empty()
            logging.info("2> phase: {}, len(packets): {}".format(phase, len(packets)))
            for packet in packets:
                self.modules["model_manager"].add_package(packet)
            self.modules["model_manager"].wait_until_empty()
            logging.info("3> phase: {}, len(packets): {}".format(phase, len(packets)))
            for packet in packets:
                self.modules["analyzer_manager"].add_package(packet)
            self.modules["analyzer_manager"].wait_until_empty()

        logging.info("Quitting the experiment")
        self.quit()

    def get_phase(self):
        return self.phase

    def write_result(self, packets, ofname):
        pass

def inet_to_str(addr):
    try:
        return socket.inet_ntop(socket.AF_INET, addr)
    except:
        return socket.inet_ntop(socket.AF_INET6, addr)

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", required=True, metavar="<configuration file>", help="Configuration File", type=str)
    parser.add_argument("-o", "--output", metavar="<output filename>", help="Output filename", type=str, default="output.csv")
    parser.add_argument("-l", "--log", metavar="<log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)>", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")
    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)

    cname = os.path.abspath(args.conf)
    logging.debug("Configuration file: {}".format(cname))
    conf = parse_config(cname)
    run = Tester(conf, args.output)

if __name__ == "__main__":
    main()
