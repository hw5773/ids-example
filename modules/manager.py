import argparse
import time
import logging
import threading
import sys
sys.path.append("..")
from iutils.encoders import init_encoders

usleep = lambda x: time.sleep(x/1000000.0)
THREAD_USLEEP_TIME = 10000
WAITING_USLEEP_TIME = 10000

class Manager:
    def __init__(self, core, name, conf):
        self.core = core
        self.name = name
        self.config = conf

        self.cnt = 1
        self.queue = []
        self.queue_lock = threading.Lock()
        self.running = True

    def add_package(self, package):
        self.queue_lock.acquire()
        package.set_serial_number(self.cnt)
        self.queue.append(package)
        self.cnt += 1
        logging.debug("add_packet(): self.cnt: {} (len(self.queue): {})".format(self.cnt, len(self.queue)))
        self.queue_lock.release()
            
    def wait_until_empty(self):
        while len(self.queue) > 0:
            usleep(WAITING_USLEEP_TIME)

    def get_queue_length(self):
        return len(self.queue)

    def get_name(self):
        return self.name

    def quit(self):
        self.running = False

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Configuration file", type=str, default="sig.conf")
    parser.add_argument("-l", "--log", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")

    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    logging.basicConfig(level=args.log)

if __name__ == "__main__":
    main()
