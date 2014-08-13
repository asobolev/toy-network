import numpy as np
import simplejson as json
from reduced.setup import *

setup_classes = [ISGStraightSetup, NeuronSetup, SynapseHomSetup,
                 SynapseHomNormSetup, ConnectionSetup]


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


def weights_as_matrix(synapse_list):
    """
    Extracts a 2D array of weights from a list of given Synapse objects.

    :param synapse_list:    list of Synapse objects
    :return:                2D numpy array of weights
    """
    sources = [x['source'] for x in synapse_list]
    sources = sorted(set(sources), key=sources.index)

    source_filter = lambda x: x['source'] == source
    get_weights = lambda synapses: [x['weight'] for x in synapses]

    return np.array([get_weights(filter(source_filter, synapse_list)) for source in sources])