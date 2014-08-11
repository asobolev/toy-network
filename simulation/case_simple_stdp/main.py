# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# The following article builds a toy-network with two layers of neurons, aimed at learning a simple discrimination of the input stimuli. The network has 5x5 square input layer (25 input neurons), plastic (all-to-all) synaptic connections to a 5x5 map layer (25 neurons). The map layer neurons exhibit some random inhibition and local (neihboring) excitation within the layer to include some competition between the neurons.

# <markdowncell>

# All configurations for neurons, connections and synapses are located in the configurations.json (JSON) file in the case folder.

# <headingcell level=3>

# Network Setup

# <markdowncell>

# Using the related configuration, assemble the toy-network:

# <codecell>

#!/usr/bin/env python

import nest
import numpy as np

from reduced.network.network import ToyNetwork
from reduced.simulation.utils import from_file, parse_to_objects

nest.ResetKernel()

setup_dict = parse_to_objects(from_file('configurations.json'))

network_setup = [
    setup_dict['GKLEARN_5X5_0'], setup_dict['INPUT_NEURON'],
    setup_dict['MAP_NEURON'], setup_dict['HOM_SYNAPSE'],
    setup_dict['FWD_CONN'], setup_dict['INH_CONN'], setup_dict['EXC_CONN']
]
network = ToyNetwork(*network_setup)

weights_before = np.array(network.input_layer.weights)  # remember original weights

# <headingcell level=3>

# Learning

# <markdowncell>

# Simulate until the weights are converged:

# <codecell>

max_simulation_time = 5000
time_bin = 10000
convergence_delta = 5  # criteria for convergence

time_passed = 0
weights_diff = np.array(network.input_layer.weights)
previous_weights = np.array(network.input_layer.weights)

while (time_passed < max_simulation_time) and not (weights_diff < convergence_delta).all():
    nest.Simulate(time_bin)
    time_passed += time_bin
    
    actual_weights = np.array(network.input_layer.weights)
    weights_diff = np.abs(actual_weights - previous_weights)
        
    previous_weights = actual_weights
    
print time_passed

# <codecell>

from reduced.simulation.plot.weights import weights_multiple

weights_after = np.array(network.input_layer.weights)

fig = weights_multiple([weights_before, weights_after])

# <headingcell level=3>

# Testing

# <markdowncell>

# Set voltage monitors before the simulation:

# <codecell>

from reduced.network.monitors import VoltageMonitor, MonitorPool, SpikeDetector

#input_monitors = MonitorPool(VoltageMonitor, network.input_layer.nodes)
#map_monitors = MonitorPool(VoltageMonitor, network.map_layer.nodes)

spike_detector = SpikeDetector(network.map_layer.nodes)

# <markdowncell>

# Simulate sample interval:

# <codecell>

nest.Simulate(5000)

# <markdowncell>

# Compare outputs:

# <codecell>

import matplotlib.pyplot as plt

from nest import raster_plot
from reduced.simulation.plot.dynamics import layer_co_dynamics

#events_i = np.array([vm.V_m for vm in input_monitors])
#events_m = np.array([vm.V_m for vm in map_monitors])

#fig1 = layer_co_dynamics(events_i, events_m, input_monitors[0].times)

fig2 = raster_plot.from_device([spike_detector.id], hist=True)

# <codecell>

plt.show()

