import nest

from base import NestObject
from synapse import Synapse


class Neuron(NestObject):

    def __init__(self, nest_id):
        super(Neuron, self).__init__(nest_id)

    def __repr__(self):
        return "NEST Neuron (%d) with %d connections" % \
               (self.id, len(self.synapses))

    def synapse_with(self, neurons, weights, delay=1.0, model='static_synapse'):
        """
        Create synaptic connections with given neurons.         
        
        :param neurons:     a list of Neuron objects
        :param weights:     a list of weights for every new synapse (float)
        :param delay:       delay (float)
        :param model:       model of the synapse (string)
        """
        target_ids = [x.id for x in neurons]
        nest.DivergentConnect([self.id], target_ids, weights, delay, model)

    @property
    def synapses(self):
        """
        Synapse objects are always re-created as new connections could be
        created outside of the Neuron object. NEST feature..

        :return:    list of Synapse objects (includes synapse with Layer)
        """

        # TODO exclude connection with Layer
        nodes = nest.GetConnections([self.id])
        return [Synapse(*list(node)) for node in nodes]
