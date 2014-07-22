from __future__ import absolute_import
import reduced.setup.configurations as conf


INPUT = {
    'GKLEARN_5X5_0': conf.ISGStraightGaussKernel('data/5x5gklearn0.idlmov'),
    'GKLEARN_5X5_1': conf.ISGStraightGaussKernel('data/5x5gklearn1.idlmov')
}


NEURONS = {
    'INPUT_NEURON': conf.InputNeuron()
}
