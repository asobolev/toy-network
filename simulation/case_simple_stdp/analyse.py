#!/usr/bin/env python

"""
Creates a weight evolution figure for a small subset of map neurons. A figure
contains a raster plot of input layer spiking (top) together with the weight
evolution map (bottom) for selected neuron(s).
"""

import argparse
import h5py
import numpy as np

from reduced.simulation.utils import with_data
from reduced.simulation.plot.weights import *
from reduced.simulation.plot.dynamics import raster_plot


@with_data
def weights_before_and_after(f, t1=0, t2=-1):
    """
    Plots actual weights between input and map at two points in time

    :param f:   file path with recorded weights data
    :param t1:  first timepoint as int
    :param t2:  second timepoint as int
    """
    all_datasets = filter(lambda x: 'target' in x.attrs.keys(), f['synapses'].values())

    sources = [x.attrs['source'] for x in all_datasets]
    sources = sorted(set(sources), key=sources.index)
    source_filter = lambda src: filter(lambda x: x.attrs['source'] == src, all_datasets)

    weights_at_time = lambda t: [[w[t] for w in source_filter(src)] for src in sources]

    weights_before = weights_at_time(t1)
    weights_after = weights_at_time(t2)

    return weights_multiple([weights_before, weights_after])


@with_data
def raster(f, map_or_input='map'):
    """
    Render raster plot for spikes for a given layer

    :param f:               file path with recorded weights data
    :param map_or_input:    'map' or 'input'
    """
    times = f['spikes_%s' % map_or_input]['times']
    senders = f['spikes_%s' % map_or_input]['senders']

    return raster_plot(np.array(times), np.array(senders))


@with_data
def weight_dynamics_for_single(f, target_index=0):
    """
    Render weight dynamics for a particular map layer neuron

    :param f:               file path with recorded weights data
    :param target_index:    index of the map layer neuron to plot weights for
    """
    all_datasets = filter(lambda x: 'target' in x.attrs.keys(), f['synapses'].values())

    targets = [x.attrs['target'] for x in all_datasets]
    targets = sorted(set(targets), key=targets.index)

    selected = targets[target_index]  # NEST id of the map layer neuron

    datasets = filter(lambda x: x.attrs['target'] == selected, all_datasets)
    weights = np.array([np.array(w) for w in datasets])

    return single_weight_evolution(weights, str(selected))


# voltage dynamics of a particular neuron

if 0:
    with h5py.File('weights.h5', 'r') as f:
        #multiple_time_series(events, times)
        pass



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyse')

    parser.add_argument('--file', type=str, default='weights.h5')

    parser.add_argument('-w, --weights', dest='weights', action='store_true')
    parser.add_argument('-t1', type=int, default=0)
    parser.add_argument('-t2', type=int, default=-1)

    parser.add_argument('-r, --raster', dest='raster', type=str)

    args = parser.parse_args()
    if args.weights:
        weights_before_and_after(args.file, t1=args.t1, t2=args.t2)
    if args.raster:
        raster(args.file, map_or_input=args.raster)

    plt.show()

