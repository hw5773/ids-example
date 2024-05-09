from definitions.window import Window
from definitions.packet import Packet
import logging
import copy
import time

class Packages:
    def __init__(self):
        self.type = None
        self.packages = []
        self.cnt = 0

    def add_package(self, package):
        self.packages.append(package)
        if self.cnt == 0:
            if isinstance(package, Window):
                self.type = "window"
            elif isinstance(package, Packet):
                self.type = "packet"

    def get_type(self):
        return self.type

    def get_packages(self):
        return self.packages

    def get_packages_length(self):
        return len(self.packages)

    def get_dataset(self):
        dataset = []

        for p in self.packages:
            dataset.append(p.get_code())

        return dataset

    def get_labels(self):
        labels = []

        for p in self.packages:
            labels.append(p.get_label(kind))

        return labels
