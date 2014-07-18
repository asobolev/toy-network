from __future__ import absolute_import
from reduced.setup.configurations import neurons, input


def build_input_configurations():
    GKLEARN_5X5_0 = input.ISGStraightGaussKernel()
    GKLEARN_5X5_0.movie_path = 'data/5x5gklearn0.idlmov'

    GKLEARN_5X5_1 = input.ISGStraightGaussKernel()
    GKLEARN_5X5_1.movie_path = 'data/5x5gklearn1.idlmov'

    return {
        'GKLEARN_5X5_0': GKLEARN_5X5_0,
        'GKLEARN_5X5_1': GKLEARN_5X5_1
    }


INPUT = build_input_configurations()
NEURONS = {'INPUT_NEURON': neurons.InputNeuron()}
