import nest
import nest.topology as tp


class ConnectionPool(object):
    """
    A base class for connections between two layers of neurons.
    """
    def __init__(self, source, target, conn_setup, initial_weights=None):
        """
        Constructor of connections pool between two layers.

        :param source:          a Layer object
        :param target:          a Layer object
        :param conn_setup:      ConnectionSetup object with connection params
        :param initial_weights: a list of initials weights to set
        """
        self.source = source
        self.target = target
        self.initial_weights = initial_weights

        import ipdb
        ipdb.set_trace()

        # TODO check if this returns IDs
        tp.ConnectLayers(source, target, conn_setup.as_nest_dict)

        self.nodes = nest.GetConnections(source.nodes, target.nodes)
        if initial_weights:
            nest.SetStatus(self.nodes, 'weight', initial_weights)

    def get_connection(self, x, y):
        # TODO
        pass

    def get_weight(self, x, y):
        return nest.GetStatus(self.get_connection(x, y), 'weight')[0]