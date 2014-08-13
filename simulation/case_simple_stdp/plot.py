#!/usr/bin/env python

"""
Creates a weight evolution figure for a small subset of map neurons. A figure
contains a raster plot of input layer spiking (top) together with the weight
evolution map (bottom) for selected neuron(s).
"""

import h5py
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.pyplot import figure
from reduced.simulation.plot.weights import *
from reduced.simulation.plot.dynamics import raster_plot


fig = figure(figsize=(15, 10))

ax_r = fig.add_subplot(211)  # axes to plot input as raster plot
ax_w = fig.add_subplot(212)  # axes to plot weight evolution
ax_c = fig.add_axes([0.1, 0.1, 0.8, 0.05])  # axes for colorbar

# render raster plot with input layer spikes

with h5py.File('weights.h5', 'r') as f:
    times = f['spikes']['times']
    senders = f['spikes']['senders']

    raster_plot(ax_r, times, senders)


# render weight dynamics for a particular map layer neuron

with h5py.File('weights.h5', 'r') as f:
    all_datasets = filter(lambda x: 'target' in x.attrs.keys(), f['synapses'].values())

    targets = [x.attrs['target'] for x in all_datasets]
    targets = sorted(set(targets), key=targets.index)

    selected = targets[0]  # NEST id of the map layer neuron

    datasets = filter(lambda x: x.attrs['target'] == selected, all_datasets)
    weights = np.array([np.array(w) for w in datasets])


image = render_rectangular_matrix(ax_w, weights, 'time (ms)', 'input neurons')

g_min = weights.min()
delta = weights.max() - g_min
labels = [round((g_min + (x * delta/10.0)), 2) for x in range(11)]

render_colorbar(image, ax_c, 'horizontal', labels)


title = 'Weight evolution for neuron %s' % str(selected)
fig.canvas.set_window_title(title)

plt.show()

