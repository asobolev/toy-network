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


fig = figure(figsize=(15, 10))

ax_r = fig.add_subplot(211)  # axes to plot input as raster plot
ax_w = fig.add_subplot(212)  # axes to plot weight evolution


# render raster plot with input layer spikes

with h5py.File('weights.h5', 'r') as f:
    times = f['spikes']['times']
    senders = f['spikes']['senders']

raster_plot(ax_r, times, senders)


# render weight dynamics for a particular map layer neuron

with h5py.File('weights.h5', 'r') as f:
    all_datasets = filter(lambda x: 'target' in x.attr.keys(), f['synapses'])

    targets = [x.attr['target'] for x in all_datasets]
    targets = sorted(set(targets), key=targets.index)

    selected = targets[0]  # NEST id of the map layer neuron

    datasets = filter(lambda x: x['target'] == selected, all_datasets)
    weights = [np.array(w) for w in datasets]

weights_evolution(ax_w, weights)


title = 'Weight evolution for neuron %s' % str(target_id)
fig.canvas.set_window_title(title)

plt.show()

