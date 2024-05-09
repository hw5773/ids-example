import os
import sys
import argparse
import logging
from iutils.etc import camel_code

def prepare_names(name):
    ndir = "{}".format(name)
    names = []
    files = [f for f in os.listdir(ndir) if f.endswith(".py") and f != "{}.py".format(name[0:-1])]

    for f in files:
        names.append(f.split(".")[0])

    return names

def make_initializers(names):
    for name in names:
        lst = names[name]
        with open("iutils/{}.py".format(name), "w") as of:
            of.write("import sys\n")
            of.write("sys.path.append(\"..\")\n")
        
            for e in lst:
                of.write("from {}.{} import {}\n".format(name, e, camel_code(e)))

            of.write("\n")
            of.write("def init_{}({}_manager):\n".format(name, name[:-1]))

            for e in lst:
                of.write("    {}_manager.add_{}({}(\"{}\"))\n".format(name[:-1], name[:-1], camel_code(e), e))

def make_config(ofname, names):
    with open(ofname, "w") as of:
        of.write("packet_capturer:\n")
        of.write("\ttraining_packets: data/training.pcap\n")
        of.write("\ttraining_label: data/training.label\n")
        of.write("\ttesting_packets: data/testing.pcap\n")
        of.write("\ttesting_label: data/testing.label\n\n")

        of.write("window_manager:\n")
        of.write("\twindow_length: 1\n")
        of.write("\tsliding_interval: 0.1\n\n")

        of.write("feature_extractor:\n")
        features = names["features"]
        for feature in features:
            of.write("\t{}: true\n".format(feature))
        of.write("\n")
        

        of.write("encoder_manager:\n")
        of.write("\tname: {}\n\n".format(names["encoders"][0]))
        
        of.write("model_manager:\n")
        of.write("\tname: {}\n\n".format(names["models"][0]))

def command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--encoders", help="Encoder directory", type=str, default="encoders")
    parser.add_argument("-f", "--features", help="Feature directory", type=str, default="features")
    parser.add_argument("-m", "--models", help="Model directory", type=str, default="models")
    parser.add_argument("-o", "--output", help="Output file name", type=str, default="config.yaml")
    parser.add_argument("-l", "--log", help="Log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)", default="INFO", type=str)
    args = parser.parse_args()
    return args

def main():
    args = command_line_args()

    if not os.path.exists(args.encoders):
        print ("Invalid encoder directory. Please insert the correct encoder directory")
        sys.exit(1)

    if not os.path.exists(args.models):
        print ("Invalid model directory. Please insert the correct model directory")
        sys.exit(1)

    logging.basicConfig(level=args.log)

    names = {}
    enames = prepare_names(args.encoders)
    names[args.encoders] = enames
    logging.debug("encoders: {}".format(enames))
    fnames = prepare_names(args.features)
    names[args.features] = fnames
    logging.debug("features: {}".format(fnames))
    mnames = prepare_names(args.models)
    names[args.models] = mnames
    logging.debug("models: {}".format(mnames))

    make_initializers(names)
    make_config(args.output, names)

if __name__ == "__main__":
    main()
