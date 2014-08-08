import simplejson as json
from reduced.setup import *

setup_classes = [ISGStraightSetup, NeuronSetup, SynapseHomSetup,
                 ForwardConnectionSetup, InhibitoryConnectionSetup,
                 ExcitatoryConnectionSetup]


def from_file(path):
    with open(path) as f:
        return json.loads(f.read())


def parse_to_objects(conf_dict):
    def get_class(name):
        return filter(lambda x: x.__name__ == name, setup_classes)[0]

    setup_objects = {}
    for k, v in conf_dict.items():
        cls = get_class(k)

        for name, setup_dict in v.items():
            setup_objects[name] = cls(**setup_dict)

    return setup_objects