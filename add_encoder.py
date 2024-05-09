import argparse
import sys
import os
from iutils.etc import camel_code

def generate_template(name):
    fname = "encoders/{}.py".format(name)

    with open(fname, "w") as f:
        f.write("import sys\n")
        f.write("import logging\n")
        f.write("from encoders.encoder import Encoder\n\n")
        f.write("class {}(Encoder):\n".format(camel_code(name)))
        f.write("    def __init__(self, name):\n")
        f.write("        super().__init__(name)\n\n")
        f.write("    # Please implement the following function\n")
        f.write("    # The variable `ret` should contain the result value\n")
        f.write("    def encode(self, packet):\n")
        f.write("        # TODO: Implement the procedure to detect anomaly based on the signature\n")
        f.write("        code = []\n")
        f.write("\n")
        f.write("\n")
        f.write("        logging.debug('{}: {}'.format(self.get_name(), code))\n")
        f.write("        packet.set_code(self.get_name(), code)\n")


def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help="Signature name", type=str)
    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    name = args.name

    fname = "signatures/{}.py".format(name)

    if os.path.exists(fname):
        print ("The same name of the signature exists. Please insert another name for the signature to be defined")
        sys.exit(1)

    generate_template(name)

if __name__ == "__main__":
    main()
