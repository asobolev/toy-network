import nest

from base import NestObject
from synapse import Synapse


class Neuron(NestObject):

    def __init__(self, neuron_setup):
        nest_id = nest.Create(neuron_setup.model, params=neuron_setup.para_dict)[0]

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
        syn_spec = lambda w: {'weight': w, 'model': model, 'delay': delay}

        target_ids = [x.id for x in neurons]
        for neuron_id, weight in zip(target_ids, weights):
            nest.Connect([self.id], [neuron_id], syn_spec=syn_spec(weight))

    @property
    def synapses(self):
        """
        Synapse objects are always re-created as new connections could be
        created outside of the Neuron object. NEST feature..

        :return:    list of Synapse objects (includes synapse with Layer)
        """
        connections = nest.GetConnections([self.id])

        # define a filter for non-neuron connections (spike detectors etc.)
        get_conn_type = lambda conn: nest.GetStatus([conn[1]], 'node_type')[0]
        is_synapse = lambda conn: get_conn_type(conn).name == 'neuron'

        synaptic_connections = filter(is_synapse, connections)
        return [Synapse(*list(node)) for node in synaptic_connections]
