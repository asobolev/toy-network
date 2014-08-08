from __future__ import absolute_import
from reduced.setup.neurons import NeuronSetup
from reduced.setup.inputs import ISGStraightSetup


#-----------------
# Image generators
#-----------------

GKLEARN_5X5_0 = ISGStraightSetup(**{
    'stimuli_duration': 50.0,
    'i_s_i': 50.0,
    'movie_path': '../data/5x5gklearn0.idlmov'
})

#--------
# Neurons
#--------

INPUT_NEURON = NeuronSetup(**{
    'model': 'pixel_iaf_psc_exp',
    'para_dict': {},
    'lat_ex_input_ports': [],
    'noise_firing_rate': 12000.,
    'noise_amplitude': 13.9  # 3 Hz background noise
})