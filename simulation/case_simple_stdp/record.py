#!/usr/bin/env python

"""
This script is aimed to record the evolution of weights between input and map
layer neurons. It runs the simulation in small time steps and records weights
after every stimulus presentation.
"""

import nest
import h5py
import numpy as np

from reduced.network.network import ToyNetwork
from reduced.simulation.utils import *

#--------------
# Network setup
#--------------

nest.ResetKernel()

setup_dict = parse_to_objects(from_file('configurations.json'))

network_setup = [
    setup_dict['GKLEARN_5X5_0'], setup_dict['INPUT_NEURON'],
    setup_dict['MAP_NEURON'], setup_dict['HOM_SYNAPSE'],
    setup_dict['FWD_CONN'], setup_dict['INH_CONN'], setup_dict['EXC_CONN']
]
network = ToyNetwork(*network_setup)

#---------
# Learning
#---------

phase = setup_dict['GKLEARN_5X5_0'].i_s_i + setup_dict['GKLEARN_5X5_0'].stimuli_duration

max_simulation_time = 15000
time_passed = 0

spider = []  # collector for actual synaptic states (weights)
times = []   # records times when states were collected

get_as_dict = lambda synapses: [x.as_dict() for x in synapses]

#--------------------------------------------------------
# Simulate with cycles equal to one stimulus presentation
#--------------------------------------------------------

while time_passed < max_simulation_time:
    nest.Simulate(phase)
    time_passed += phase

    spider.append(get_as_dict(network.input_layer.synapses))
    times.append(time_passed)

#-------------------
# Dump synaptic data
#-------------------

synapse_sample = spider[0]
synapse_ids = [(x['source'], x['target']) for x in synapse_sample]

weights = np.array([[x['weight'] for x in synapses] for synapses in spider])

with h5py.File('weights.h5', 'w') as f:
    all_synapses = f.create_group('synapses')

    for i, id_pair in enumerate(synapse_ids):
        source, target = id_pair  # source, target are NEST ids

        name = "%s-%s" % (str(source), str(target))
        data = [x[i] for x in weights]
        syn = all_synapses.create_dataset(name, data=data)

        syn.attrs.create('source', source)
        syn.attrs.create('target', target)

    f.create_dataset('times', data=np.array(times))