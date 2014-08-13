
"""
for a small subset of map neurons.
 Plots with
weight values evolution are created as a result of this analysis.
"""

#----------------------------------
# Plot weights for selected neurons
#----------------------------------


from reduced.simulation.plot.weights import weights_multiple

weights_before = weights_as_matrix(spider[0])
weights_after = weights_as_matrix(spider[-1])

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

