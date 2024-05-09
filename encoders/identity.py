import sys
import logging
from encoders.encoder import Encoder

class Identity(Encoder):
    def __init__(self, name):
        super().__init__(name)

    # Please implement the following function
    # The variable `ret` should contain the result value
    def encode(self, packet):
        # TODO: Implement the procedure to detect anomaly based on the signature
        code = []

        logging.debug('{}: {}'.format(self.get_name(), code))
        packet.set_code(self.get_name(), code)
