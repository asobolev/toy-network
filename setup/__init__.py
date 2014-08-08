from __future__ import absolute_import
from reduced.setup.inputs import ISGStraightSetup
from reduced.setup.neurons import NeuronSetup
from reduced.setup.synapses import SynapseHomSetup
from reduced.setup.connections import ForwardConnectionSetup, \
    InhibitoryConnectionSetup, ExcitatoryConnectionSetup

__all__ = ['ISGStraightSetup', 'NeuronSetup', 'SynapseHomSetup',
           'ForwardConnectionSetup', 'InhibitoryConnectionSetup',
           'ExcitatoryConnectionSetup']