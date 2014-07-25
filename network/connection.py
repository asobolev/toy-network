import numpy as np
import nest
import nest.topology as tp


class ConnectionPool(object):
    """
    A base class for connections between two layers of neurons.
    Simple all-to-all connection between given layers.

    Weights are immutable in this class.
    """
    def __init__(self, source, target, conn_setup, initial_weights=None):
        """
        Constructor of connections pool between two layers.

        :param source:          a Layer object
        :param target:          a Layer object
        :param conn_setup:      ConnectionSetup object with connection params
        :param initial_weights: a list of initials weights to set
        """
        self._source = source
        self._target = target
        self._initial_weights = initial_weights

        tp.ConnectLayers([source.id], [target.id], conn_setup.as_nest_dict)

        self._nodes = np.array(nest.GetConnections(source.nodes, target.nodes))

        if initial_weights:
            nest.SetStatus(self._nodes, 'weight', initial_weights)

    def __len__(self):
        return len(self._source.nodes)

    def __getitem__(self, key):
        """
        Get connections by source node index.

        TODO find out if it's faster to query GetStatus all the nodes at once
        if the full array of connections is needed.

        :param key: index of the source layer node
        :return:    array of connections [(target-gid, weight), ...]
        """
        node_id = self._source.nodes[key]
        nodes = filter(lambda x: x[0] == node_id, self._nodes)

        states = nest.GetStatus(nodes)
        return np.array([[x['source'], x['target'], x['weight']] for x in states])

    def __iter__(self):
        for i in range(0, len(self)):
            yield self.__getitem__(i)

    def __delitem__(self, key):
        raise NotImplementedError()

    def __str__(self):
        return str(np.array(list(self)))

    def __repr__(self):
        return str(self)

    @property
    def weights(self):
        """
        returns 2D array of actual weights (1D - source, 2D - target nodes)
        """
        return np.array([x[:,2] for x in list(self)])

    @property
    def weights_normalized(self):
        """
        returns 2D array of actual weights (1D - source, 2D - target node)
        normalized to values between 0.0 and 1.0. Useful for plotting
        """
        all_weights = self.weights
        return all_weights / (all_weights.max())