import nest
import random
import numpy as np
import itertools as it

from reduced.network.layer import InputLayer, MapLayer


class ToyNetwork(object):

    def __init__(self, ISG_SETUP, INPUT_NEURON, MAP_NEURON, SYNAPSE, FWD_CONN,
                 INH_CONN, EXC_CONN=None):
        """
        Build a new toy network. Example of configurations required to build
        a network are located in configuration files.

        :param ISG_SETUP:       Setup object for image sequence generator
        :param INPUT_NEURON:    Setup object for input neurons
        :param MAP_NEURON:      Setup object for map neurons
        :param SYNAPSE:         Setup object for synapses between input and map
        :param FWD_CONN:        Setup object for connections between input and
                                map
        :param INH_CONN:        Setup object for inhibition in the map layer
        :param EXC_CONN:        Setup object for excitation in the map layer
        :return:
        """

        self._input_layer = InputLayer(2000., ISG_SETUP, INPUT_NEURON)
        self._map_layer = MapLayer(MAP_NEURON)

        # plastic connections from input to map layer
        nest.CopyModel(FWD_CONN.model, 'plastic', SYNAPSE.as_nest_dict)

        targets = [x for x in self._map_layer]
        for neuron in self._input_layer:
            weights = [float(x) for x in (FWD_CONN.wmax * np.random.rand(len(targets)))]
            neuron.synapse_with(targets, weights, model='plastic')

        # static random inhibitory connections in the map layer
        for neuron in self._map_layer:
            # may include itself
            some = random.sample(self._map_layer, INH_CONN.quantity)
            neuron.synapse_with(some, INH_CONN.weight, model=INH_CONN.model)

        import ipdb
        ipdb.set_trace()

        # excitatory connections to neighboring neurons
        for x, row in enumerate(self._map_layer.as_matrix):
            for y, neuron in enumerate(row):
                horizontal = (x-1, x, x+1 if x+1 < self._map_layer.x_dim else -1)
                vertical = (y-1, y, y+1 if y+1 < self._map_layer.y_dim else -1)
                coords = it.product(horizontal, vertical)
                coords = filter(lambda q: not q == (x, y), coords)

                neighbors = [self._map_layer.as_matrix[i][j] for i, j in coords]
                neuron.synapse_with(neighbors, EXC_CONN.weight, model=EXC_CONN.model)

    @property
    def input_layer(self):
        return self._input_layer

    @property
    def map_layer(self):
        return self._map_layer
