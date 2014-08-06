import itertools
import nest
import nest.topology as tp
import numpy as np

from base import NestObject
from neuron import Neuron


class Layer(NestObject):

    def __init__(self, neuron_setup, x_dim=5, y_dim=5):
        """
        Constructor of the base layer. A base layer is a flat 2D layer with
        neurons of a given model (parameters) and built-in spike detector.

        :param neuron_setup:    NeuronSetup object with settings for the
                                neurons for the layer
        :param x_dim:           number of neurons in X-dimension
        :param y_dim:           number of neurons in Y-dimension
        """
        self._x_dim = x_dim
        self._y_dim = y_dim

        nest_id = tp.CreateLayer({
            'rows': x_dim,
            'columns': y_dim,
            'elements': neuron_setup.model,
            'edge_wrap': True
        })[0]
        super(Layer, self).__init__(nest_id)

        node_ids = nest.GetNodes([self._nest_id])[0]
        self._neurons = [Neuron(nid) for nid in node_ids]

        self._spikes = nest.Create('spike_detector', 1, [{'label': 'input_spikes'}])[0]
        nest.ConvergentConnect(self.nodes, [self._spikes])

    # methods to access neurons as a list

    def __len__(self):
        return len(self._neurons)

    def __getitem__(self, key):
        return self._neurons[key]

    def __iter__(self):
        for i in range(0, len(self)):
            yield self.__getitem__(i)

    def __delitem__(self, key):
        raise NotImplementedError()

    def __str__(self):
        return str((list(self)))

    def __repr__(self):
        return str(self)

    # 2D access interface

    @property
    def x_dim(self):
        return self._x_dim

    @property
    def y_dim(self):
        return self._y_dim

    @property
    def as_matrix(self):
        """
        Returns a 2D list with related neuron objects. Makes it easier to access
        element by (x, y) coordinate, like

        Layer[x][y]

        :return:    2D list of related Neuron objects
        """
        start_indices = [self._y_dim*i for i in range(self._x_dim)]
        return [self[i:i + self._y_dim] for i in start_indices]

    # weights access

    @property
    def weights(self):
        """
        returns 2D array of actual weights (1D - source, 2D - target nodes)
        """
        weights = [[x['weight'] for x in neuron.synapses] for neuron in self]
        return np.array(weights)

    # helper methods

    @property
    def nodes(self):
        return [x.id for x in self._neurons]

    # spike detector interface

    @property
    def spikes(self):
        return self._spikes

    def clear_spike_detector(self):
        nest.SetStatus([self._spikes], 'n_events', 0)


class InputLayer(Layer):

    def __init__(self, input_weight, ISG_setup, neuron_setup, x_dim=5, y_dim=5):
        """
        Constructor of the input layer. An input layer is a flat layer with
        neurons that fire according to the intensity of the presented images as
         sequence in time. Images are parsed from the given movie file inside
         ImageSequenceGeneratorSetup settings.

        :param input_weight     weight for the connections between the image
                                generator and the neurons
        :param ISG_setup:       ImageSequenceGeneratorSetup object with image
                                parsing settings
        """
        super(InputLayer, self).__init__(neuron_setup, x_dim, y_dim)

        self._movie = nest.Create(
            'image_sequence_generator', 1, ISG_setup.as_nest_dict
        )[0]

        nodes = iter(self.nodes)
        for x, y in itertools.product(range(x_dim), range(y_dim)):
            node = nodes.next()
            nest.SetStatus([node], {'x': x, 'y': y, 'weight': input_weight})
            nest.Connect([self._movie], [node])


class MapLayer(Layer):
    pass
