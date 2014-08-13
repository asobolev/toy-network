#!/usr/bin/env python

"""
Creates a weight evolution figure for a small subset of map neurons. A figure
contains a raster plot of input layer spiking (top) together with the weight
evolution map (bottom) for selected neuron(s).
"""

import h5py
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from reduced.simulation.plot.weights import weights_multiple
from reduced.simulation.plot.dynamics import raster_plot


# read out all IDs of the map layer neurons

with h5py.File('weights.h5', 'r') as f:
    datasets = filter(lambda x: 'target' in x.attr.keys(), f['synapses'])

    targets = [x.attr['target'] for x in datasets]
    targets = sorted(set(targets), key=targets.index)


target_id = targets[0]  # NEST id of the map layer neuron

title = 'Weight evolution for neuron %s' % str(target_id)

fig = figure(figsize=(15, 10))
fig.canvas.set_window_title(title)

ax_r = fig.add_subplot(211)  # axes to plot input as raster plot
ax_w = fig.add_subplot(212)  # axes to plot weight evolution

with h5py.File('weights.h5', 'r') as f:
    times = f['spikes']['times']
    senders = f['spikes']['senders']

    raster_plot(ax_r, times, senders)




plt.show()

