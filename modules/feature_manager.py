import argparse
import time
import logging
import threading
import os
import sys
sys.path.append("..")
from modules.manager import *
from iutils.etc import parse_config
from iutils.features import init_features
from definitions.packet import Packet
from definitions.window import Window

class FeatureManager(Manager):
    def __init__(self, core, name, conf):
        super().__init__(core, name, conf)
        self.features = {}
        init_features(self)

        sd = threading.Thread(target=self.run, daemon=True)
        sd.start()

    def add_feature(self, feature):
        if feature.get_name() in self.config:
            self.features[feature.get_name()] = feature
            logging.debug("Feature {} is loaded".format(feature.get_name()))

    def run(self):
        logging.info("Run {}".format(self.name))

        while self.running or len(self.queue)>0:
            usleep(THREAD_USLEEP_TIME)
            if len(self.queue) > 0:
                self.queue_lock.acquire()
                package = self.queue.pop(0)
                logging.info("run(): self.cnt: {} (len(self.queue): {})".format(self.cnt, len(self.queue)))

                if isinstance(package, Packet):
                    self.extract(package)
                elif isinstance(package, Window):
                    logging.error("not supported one")
                self.queue_lock.release()

    def extract(self, package):
        logging.debug("extract()")
        for e in self.features:
            self.features[e].extract(package)
            logging.debug("encoded code: {}".format(package.get_code(self.features[e].get_name())))

    def quit(self):
        self.running = False

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Configuration file", type=str, default="ids.conf")
    parser.add_argument("-p", "--port", help="Port number", type=int, default=1234)
    parser.add_argument("-l", "--log", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")

    args = parser.parse_args()
    return args

def main():
    args = command_line_args()

    logging.basicConfig(level=args.log)

    if not os.path.exists(args.config):
        logging.error("Configuration file does exist: {}".format(args.config))
        sys.exit(1)

    conf, modules = parse_config(args.config)
    name = "EncoderManager"
    encoder_manager = EncoderManager(None, name, conf.get(name, None))

if __name__ == "__main__":
    main()
