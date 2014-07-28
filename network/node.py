import nest
from base import NestObject
from synapse import Synapse


class Neuron(NestObject):

    _synapses = []

    def __repr__(self):
        if self._synapses:
            synapses = ", ".join([str(x) for x in self._synapses])
            return "NEST Neuron (%d) with connections: %s" % (self.id, synapses)
        else:
            return "NEST Neuron (%d) with no connections" % self.id

    def synapse_with(self, neurons, conn_setup, initial_weights=None):
        """
        Create synaptic connections with given neurons.         
        
        :param neurons:     a list of Neuron objects
        """
        nest.ConvergentConnect([self.id], neurons)

        # create new synapses
        nodes = nest.GetConnections([self.id])
        existing_ids = [x._connection_id for x in self.synapses]
        exists = lambda x: np.array([(x = y).all() for x in existing_ids]).any()
        nodes_to_add = [x for x in nodes if not exists(x)]

        for node in nodes_to_add:
            self._synapses.append(Synapse(**list(node)))

    @property
    def synapses(self):
        return self._synapses
