from __future__ import absolute_import
from reduced.setup.models import NeuronSetup, ISGStraightSetup


GKLEARN_5X5_0 = ISGStraightSetup(**{
    'stimuli_duration': 100.0,
    'i_s_i': 50.0,
    'movie_path': '../data/5x5gklearn0.idlmov'
})

GKLEARN_5X5_0_BABY = ISGStraightSetup(**{
    'stimuli_duration': 50.0,
    'i_s_i': 50.0,
    'movie_path': '../data/5x5gklearn0.idlmov'
})

GKLEARN_5X5_1 = ISGStraightSetup(**{
    'stimuli_duration': 20.0,
    'i_s_i': 200.0,
    'movie_path': '../data/5x5gklearn1.idlmov'
})

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
