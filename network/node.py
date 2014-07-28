from base import NestObject


class Neuron(NestObject):

    _synapses = []

    def __repr__(self):
        if self._synapses:
            synapses = ", ".join([str(x) for x in self._synapses])
            return "NEST Neuron (%d) with connections: %s" % (self.id, synapses)
        else:
            return "NEST Neuron (%d) with no connections" % self.id

    def synapses(self):
        return self._synapses