#!/usr/bin/env python

"""
Creates several plots according to a results of a simulation.

Example:

./analyse.py --file weights.h5 -w -r

./analyse.py --file weights.h5 -w -t1=0 -t2=25

"""

import argparse
import numpy as np

from reduced.simulation.dump import NixDumper
from reduced.simulation.plot.weights import *
from reduced.simulation.plot.dynamics import raster_plot, multiple_time_series


# ----------------
# Helper functions
# ----------------

def with_data(func):
    """
    A decorator that open an HDF5 file and passes an open File descriptor to a
    decorate func.

    :param func: function that needs an opened File
    """
    def func_with_data(path, **kwargs):
        with NixDumper(path, NixDumper.mode['readonly']) as f:
            return func(f, **kwargs)
    return func_with_data


# ------------------
# Analysis functions
# ------------------

@with_data
def weights_before_and_after(f, t1=0, t2=-1):
    """
    Plots actual weights between input and map at two points in time

    :param f:   file path with recorded weights data
    :param t1:  first timepoint as int
    :param t2:  second timepoint as int
    """
    block = f._nf.blocks[0]

    input_neurons = f.get_neurons_for_layer(block.name, 'input_layer')
    source_names = [x.name for x in input_neurons]

    is_synapse = lambda x: x.type == 'synapse'
    all_synapses = filter(is_synapse, block.data_arrays)

    has_source = lambda x, src: filter(lambda y: y.name == src, x.sources)
    syn_filter = lambda src: filter(lambda x: has_source(x, src), all_synapses)

    weights_at_time = lambda t: [[w.data[t] for w in syn_filter(src)] for src in source_names]

    weights_before = weights_at_time(t1)
    weights_after = weights_at_time(t2)

    return weights_multiple([weights_before, weights_after])


@with_data
def raster(f):
    """
    Render raster plot for all spiketrains in a file

    :param f:               file path with recorded weights data
    """
    block = f._nf.blocks[0]

    is_spiketrain = lambda x: x.type == 'spiketrain'
    spiketrains = filter(is_spiketrain, block.data_arrays)

    times = reduce(lambda x, y: x + list(y.data[:]), spiketrains, [])

    senders = []
    for st in spiketrains:
        name = st.sources[0].name
        senders += [int(name) for i in range(len(st.data))]

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


@with_data
def time_series(f, neuron_id):
    """
    Voltage dynamics of a particular neuron

    :param f:           file path with recorded weights data
    :param neuron_id:   nest ID of the neuron
    :return:
    """
    neuron = f['voltage'][str(neuron_id)]

    times = np.array(neuron['times'])
    events = np.array([neuron['values'], neuron['values']])

    return multiple_time_series(events, times)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyse')

    parser.add_argument('--file', type=str, default='weights.h5')

    parser.add_argument('-w, --weights', dest='weights', action='store_true')
    parser.add_argument('-t1', type=int, default=0)
    parser.add_argument('-t2', type=int, default=-1)

    parser.add_argument('-r, --raster', dest='raster', action='store_true')

    parser.add_argument('-d, --dynamics', dest='dynamics', type=int)

    parser.add_argument('-v, --voltage', dest='voltage', type=int)

    args = parser.parse_args()
    if args.weights:
        weights_before_and_after(args.file, t1=args.t1, t2=args.t2)
    if args.raster:
        raster(args.file)
    if args.dynamics:
        weight_dynamics_for_single(args.file, target_index=args.dynamics)
    if args.voltage:
        time_series(args.file, neuron_id=args.voltage)

    plt.show()

