import re
import os
import logging
import yaml

def camel_code(name):
    words = []

    for word in name.split("_"):
        words.append(word.capitalize())

    return ''.join(words)

def snake_code(name):
    underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
    underscorer2 = re.compile('([a-z0-9])([A-Z])')

    subbed = underscorer1.sub(r'\1_\2', name)
    return underscorer2.sub(r'\1\2', subbed).lower()

def is_int(value):
    ret = True
    try:
        int(value)
    except ValueError:
        ret = False
    return ret

def parse_config(cname):
    if not os.path.exists(cname):
        logging.error("The configuration file ({}) does not exist.".format(cname))
        sys.exit(1)

    with open(cname, "r") as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf

