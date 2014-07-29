import nest
import numpy as np


class Synapse(object):
    """
    A synapse interface to access and manage synaptic connection parameters.

    Synapse objects acts like a dict with permanent keys.
    """

    def __init__(self, source, target, thread, synapse, port):
        self._source = source
        self._target = target
        self._thread = thread
        self._synapse = synapse
        self._port = port

    @property
    def _connection_id(self):
        return np.array([self._source, self._target, self._thread,
                            self._synapse, self._port])

    def __len__(self):
        return len(self.keys())

    def __getitem__(self, key):
        return nest.GetStatus([self._connection_id], key)[0]

    def __setitem__(self, key, item):
        nest.SetStatus([self._connection_id], key, item)

    def __delitem__(self, key):
        raise NotImplementedError()

    def __iter__(self):
        for key in self.keys():
            yield key

    @staticmethod
    def keys():
        return ['synapse_model', 'target', 'weight', 'Kplus', 'delay', 
                    'source', 'receptor', 'type']

    def values(self):
        return [self[key] for key in self.keys()]

    def items(self):
        return zip(self.keys(), self.values())

