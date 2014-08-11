import simplejson as json
from reduced.setup import *

setup_classes = [ISGStraightSetup, NeuronSetup, SynapseHomSetup, ConnectionSetup]


def from_file(path):
    """
    Parses JSON file with configurations.

    :param path:    path to the JSON file
    :return:        python dict object
    """
    with open(path) as f:
        return json.loads(f.read())


def parse_to_objects(conf_dict):
    """
    Creates setup objects by parsing a given configuration dict.

    :param conf_dict:   configuration dict, with keys as setup class names and
                        values containing dicts of configuration parameters to
                        instantiate setup object of this setup type
    :return:            dict of setup objects with keys as names for each setup
                        object
    """
    def get_class(name):
        return filter(lambda x: x.__name__ == name, setup_classes)[0]

    setup_objects = {}
    for k, v in conf_dict.items():
        cls = get_class(k)

        for name, setup_dict in v.items():
            setup_objects[name] = cls(**setup_dict)

    return setup_objects