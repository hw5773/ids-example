import argparse
import time
import logging
import threading
import copy
import sys
import asyncio
sys.path.append("..")
from modules.manager import *
from iutils.etc import parse_config
from iutils.models import init_models
from definitions.packages import Packages
from definitions.packet import Packet
from definitions.window import Window
from sklearn import metrics

usleep = lambda x: time.sleep(x/1000000.0)
THREAD_USLEEP_TIME = 30000
WAITING_USLEEP_TIME = 10000

class ModelManager(Manager):
    def __init__(self, core, name, conf):
        super().__init__(core, name, conf)
        self.models = {}
        init_models(self)

        self.training_packages = Packages()
        self.testing_packages = Packages()
       
        loop = asyncio.new_event_loop()
        mm = threading.Thread(target=run, args=(self, loop,), daemon=True)
        mm.start()

    def add_model(self, model):
        self.models[model.get_name()] = model
        logging.debug("Model {} is loaded".format(model.get_name()))

    async def learning(self, package):
        self.packages.add_package(package)

        if self.get_phase() == "training" and self.cnt >= self.core.get_end_condition():
            logging.info("Before generating the model based on the packages")
            for m in self.models:
                self.models[m].learning(self.packages)
            logging.info("After generating the model based on the packages")

    async def detection(self, package):
        if package:
            result = None
            for m in self.models:
                result, prob = self.models[m].detection(package)
                package.set_predicted_label(result)
                package.set_predicted_probability(prob)
                self.testing_packages.add_package(package)

    def get_models(self):
        return self.models

async def model(mm):
    logging.info("Run Model Manager")

    while True:
        usleep(THREAD_USLEEP_TIME)
        if not mm.is_model_generated:
            try:
                package = mm.queue.pop(0)
            except:
                package = None
            await mm.learning(package)
        elif mm.core.get_is_testing():
            try:
                package = mm.queue.pop(0)
            except:
                package = None
            await mm.detection(package)

    logging.info("Quit Model Manager")

def run(mm, loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(model(mm))

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=True, help="Configuration file", type=str, default="ids.conf")
    parser.add_argument("-l", "--log", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", type=str, default="INFO")

    args = parser.parse_args()
    return args

def main():
    args = command_line_args()

    logging.basicConfig(level=args.log)
    conf, modules = parse_config(os.path.abspath(args.config))
    name = "ModelManager"
    model_manager = ModelManager(None, name, conf.get(name, None))

if __name__ == "__main__":
    main()
