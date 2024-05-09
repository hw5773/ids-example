import argparse
import sys
import os
from iutils.etc import camel_code

def generate_template(name):
    fname = "models/{}.py".format(name)

    with open(fname, "w") as f:
        f.write("import sys\n")
        f.write("import logging\n")
        f.write("from models.model import Model\n\n")
        f.write("class {}(Model):\n".format(camel_code(name)))
        f.write("    def __init__(self, name):\n")
        f.write("        super().__init__(name)\n\n")
        f.write("    # Please implement the following function\n")
        f.write("    def learning(self, vectors):\n")
        f.write("        pass\n\n")
        f.write("    def detection(self, vector):\n")
        f.write("        pass\n")


def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help="Signature name", type=str)
    args = parser.parse_args()
    return args

def main():
    args = command_line_args()
    name = args.name

    fname = "models/{}.py".format(name)

    if os.path.exists(fname):
        print ("The same name of the signature exists. Please insert another name for the signature to be defined")
        sys.exit(1)

    generate_template(name)

if __name__ == "__main__":
    main()
