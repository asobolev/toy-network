from __future__ import absolute_import
from reduced.setup.inputs import ISGStraightSetup
from reduced.setup.neurons import NeuronSetup
from reduced.setup.synapses import SynapseHomSetup
from reduced.setup.connections import ForwardConnectionSetup, InhibitoryConnectionSetup, ExcitatoryConnectionSetup


#-----------------
# Image generators
#-----------------

GKLEARN_5X5_0 = ISGStraightSetup(**{
    'stimuli_duration': 50.0,
    'i_s_i': 50.0,
    'movie_path': '../../data/5x5gklearn0.idlmov'
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

MAP_NEURON = NeuronSetup(**{
    'model': 'iaf_psc_alpha',
    'para_dict': {
        'E_L': -65.,
        'C_m': 1.0,
        'tau_m': 20.9,
        't_ref': 2.0,
        'V_th': -50.,
        'V_reset': -55.
    },
    'lat_ex_input_ports': [0]
})

#------------
# Connections
#------------

FWD_CONN = ForwardConnectionSetup(**{
    'model': 'stdp_synapse_hom',
    'wmax': 100,
})

INH_CONN = InhibitoryConnectionSetup(**{
    'model': 'static_synapse',
    'quantity': 12,
    'weight': -500.
})

EXC_CONN = ExcitatoryConnectionSetup(**{
    'model': 'static_synapse',
    'weight': -500.
})

#---------
# Synapses
#---------

HOM_SYNAPSE = SynapseHomSetup(**{
    'alpha': 0.1,
    'Wmax': 500.
})