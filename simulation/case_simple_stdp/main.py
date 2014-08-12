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

# <headingcell level=3>

# Learning

# <markdowncell>

# Simulation parameters:

# <codecell>

phase = setup_dict['GKLEARN_5X5_0'].i_s_i + setup_dict['GKLEARN_5X5_0'].stimuli_duration
cycle = 4 * phase  # this input has 4 different stimuli

max_simulation_time = 5000
convergence_delta = 5  # criteria for convergence

time_passed = 0

# collector for actual synaptic (weights) evolution
# every element is a list of synapses with actual synaptic values
spider = []

get_as_dict = lambda synapses: [x.as_dict() for x in synapses]
get_weights = lambda synapses: [x['weight'] for x in synapses]

spider.append(get_as_dict(network.input_layer.synapses))

weights_diff = np.array(get_weights(spider[0]))
previous_weights = np.array(get_weights(spider[0]))

# <markdowncell>

# Simulate with cycles equal to one stimulus presentation to record weight evolution. Simulate until the weights are converged:

# <codecell>

# and not (weights_diff < convergence_delta).all()

while (time_passed < max_simulation_time):
    nest.Simulate(phase)
    time_passed += phase
    
    spider.append(get_as_dict(network.input_layer.synapses))
    weights_diff = np.abs(np.array(get_weights(spider[-1])) - get_weights(spider[-2]))
    
print time_passed

# <codecell>

from reduced.simulation.plot.weights import weights_multiple

def extract_weights_as_2D(synapses):
    sources = [x['source'] for x in synapses]
    sources = sorted(set(sources), key=sources.index) 

    source_filter = lambda x: x['source'] == source
    
    return [get_weights(filter(source_filter, synapses)) for source in sources]

weights_before = extract_weights_as_2D(spider[0])
weights_after = extract_weights_as_2D(spider[-1])

fig = weights_multiple([weights_before, weights_after])

# <headingcell level=3>

# Single cell analysis

# <codecell>

cell = network.map_layer[2]

print cell.id

[(x['source'], x['weight']) for x in network.input_layer.synapses_for(cell)]

# <headingcell level=3>

# Testing

# <markdowncell>

# Set voltage monitors before the simulation:

# <codecell>

from reduced.network.monitors import VoltageMonitor, MonitorPool, SpikeDetector

#input_monitors = MonitorPool(VoltageMonitor, network.input_layer.nodes)
#map_monitors = MonitorPool(VoltageMonitor, network.map_layer.nodes)

#spike_detector = SpikeDetector(network.map_layer.nodes)

# <markdowncell>

# Simulate sample interval:

# <codecell>

#nest.Simulate(10000)

# <markdowncell>

# Compare outputs:

# <codecell>

import matplotlib.pyplot as plt

from nest import raster_plot
from reduced.simulation.plot.dynamics import layer_co_dynamics

#events_i = np.array([vm.V_m for vm in input_monitors])
#events_m = np.array([vm.V_m for vm in map_monitors])

#fig1 = layer_co_dynamics(events_i, events_m, input_monitors[0].times)

#fig2 = raster_plot.from_device([spike_detector.id], hist=True)

# <codecell>

#plt.show()

