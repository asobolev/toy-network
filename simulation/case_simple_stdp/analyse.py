#!/usr/bin/env python

"""
Creates a weight evolution figure for a small subset of map neurons. A figure
contains a raster plot of input layer spiking (top) together with the weight
evolution map (bottom) for selected neuron(s).
"""

import h5py
import numpy as np

from reduced.simulation.plot.weights import *
from reduced.simulation.plot.dynamics import raster_plot

# actual weights between input and map at two points in time 

if 1:
    with h5py.File('weights.h5', 'r') as f:
        all_datasets = filter(lambda x: 'target' in x.attrs.keys(), f['synapses'].values())

        sources = [x.attrs['source'] for x in all_datasets]
        sources = sorted(set(sources), key=sources.index)
        source_filter = lambda src: filter(lambda x: x.attrs['source'] == src, all_datasets)

        weights_at_time = lambda t: [[w[t] for w in source_filter(src)] for src in sources]

        weights_before = weights_at_time(0)
        weights_after = weights_at_time(-1)

        weights_multiple([weights_before, weights_after])


# render raster plot with map layer spikes
if 0:
    with h5py.File('weights.h5', 'r') as f:
        times = f['spikes_map']['times']
        senders = f['spikes_map']['senders']

        raster_plot(np.array(times), np.array(senders))


# render weight dynamics for a particular map layer neuron

if 1:
    with h5py.File('weights.h5', 'r') as f:
        all_datasets = filter(lambda x: 'target' in x.attrs.keys(), f['synapses'].values())

        targets = [x.attrs['target'] for x in all_datasets]
        targets = sorted(set(targets), key=targets.index)

        selected = targets[17]  # NEST id of the map layer neuron

        datasets = filter(lambda x: x.attrs['target'] == selected, all_datasets)
        weights = np.array([np.array(w) for w in datasets])

        single_weight_evolution(weights, str(selected))


# voltage dynamics of a particular neuron

if 0:
    with h5py.File('weights.h5', 'r') as f:
        multiple_time_series(events, times)


plt.show()

