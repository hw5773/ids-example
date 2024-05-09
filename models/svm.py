import sys
import logging
from models.model import Model

class Svm(Model):
    def __init__(self, name):
        super().__init__(name)

    # Please implement the following function
    def learning(self, vectors):
        pass

    def detection(self, vector):
        pass
