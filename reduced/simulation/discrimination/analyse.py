#!/usr/bin/env python

"""
Creates several plots according to a results of a simulation.

Usage: ./analyse.py --file <file_name> [-t1] [-t2] [-w] [-r] [-d] [-v]

Arguments:
'--file', type=str, default='weights.h5'

'-t1', type=int, default=0      start time
'-t2', type=int, default=0      end time

'-w, --weights'                 plot weights at times t1, t2
'-r, --raster'                  plot all spiketrains
'-v, --voltage'                 plot voltage dynamics
'-e, --evo'                     plot weight sum evolution
'-d, --dynamics', type=int      plot weight dynamics for a neuron with ID

Example:

./analyse.py --file sim.h5 -w -r

./analyse.py --file sim.h5 -w -t1=0 -t2=2500

"""

import argparse
import numpy as np

from scipy.interpolate import pchip

from reduced.simulation.utils import find_nearest
from reduced.simulation.dump import NixDumper
from reduced.plot.stats import *
from reduced.plot.weights import *
from reduced.plot.dynamics import raster_plot, layer_co_dynamics
from reduced.plot.dynamics import single_line


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

def weights_before_and_after(f, t1, t2):
    """
    Plots actual weights between input and map at two points in time

    :param f:   NixDumper instance with recorded weights data
    :param t1:  start time (int)
    :param t2:  end time (int)
    """
    block = f.blocks[0]

    weights = filter(lambda x: x.type == 'synapses', block.data_arrays)[0]

    time_d = filter(lambda x: x.label == 'time', weights.dimensions)[0]
    times = np.array(time_d.ticks)

    li, ri = find_nearest(times, t1, t2)

    weights_before = weights.data[:,:,li]
    weights_after = weights.data[:,:,ri]

    return weights_multiple([weights_before, weights_after])


def weight_dynamics_for_single(f, t1, t2, target_index=0):
    """
    Render weight dynamics for a particular map layer neuron

    :param f:               NixDumper instance with recorded weights data
    :param t1:              start time (int)
    :param t2:              end time (int)
    :param target_index:    index of the map layer neuron to plot weights for
    """
    block = f.blocks[0]

    weights = filter(lambda x: x.type == 'synapses', block.data_arrays)[0]

    target_d = filter(lambda x: x.label == 'targets', weights.dimensions)[0]
    time_d = filter(lambda x: x.label == 'time', weights.dimensions)[0]
    times = np.array(time_d.ticks)

    li, ri = find_nearest(times, t1, t2)
    weights = weights.data[:,target_index,li:ri]

    return single_weight_evolution(weights, str(target_d.ticks[target_index]))


def raster(f, t1, t2):
    """
    Render raster plot for all spiketrains in a file

    :param f:   NixDumper instance with recorded weights data
    :param t1:  start time (int)
    :param t2:  end time (int)
    """
    block = f.blocks[0]

    is_spiketrain = lambda x: x.type == 'spiketrain'
    spiketrains = filter(is_spiketrain, block.data_arrays)

    times = np.array(reduce(lambda x, y: x + list(y.data[:]), spiketrains, []))

    senders = []
    for st in spiketrains:
        name = st.sources[0].name
        senders += [int(name) for i in range(len(st.data))]

    compiled = np.array(zip(times, senders))
    compiled = compiled[compiled[:,0].argsort()]

    li, ri = find_nearest(compiled[:,0], t1, t2)

    return raster_plot(compiled[:,0][li:ri], compiled[:,1][li:ri])


def time_series(f, t1, t2):
    """
    Render voltage dynamics of all analogsignals in a file

    :param f:   NixDumper instance with recorded weights data
    :param t1:  start time (int)
    :param t2:  end time (int)
    """
    block = f.blocks[0]

    input_sources = f.get_neurons_for_layer(block.name, 'input_layer')
    map_sources = f.get_neurons_for_layer(block.name, 'map_layer')

    sort_key = lambda x: int(x.sources[0].name)

    filt = lambda x: x.type == 'analogsignal' and x.sources[0] in input_sources
    i_signals = sorted(filter(filt, block.data_arrays), key=sort_key)

    filt = lambda x: x.type == 'analogsignal' and x.sources[0] in map_sources
    m_signals = sorted(filter(filt, block.data_arrays), key=sort_key)

    times = np.array(i_signals[0].dimensions[0].ticks)

    li, ri = find_nearest(times, t1, t2)
    i_events = np.array([signal.data[li:ri] for signal in i_signals])
    m_events = np.array([signal.data[li:ri] for signal in m_signals])

    return layer_co_dynamics(i_events, m_events, times[li:ri])


def weight_sum_evolution(f, t1, t2):
    """
    Evolution of the sum of weights in time.

    :param f:   NixDumper instance with recorded weights data
    :param t1:  start time (int)
    :param t2:  end time (int)
    """
    block = f.blocks[0]

    weights = filter(lambda x: x.type == 'synapses', block.data_arrays)[0]

    time_d = filter(lambda x: x.label == 'time', weights.dimensions)[0]
    times = np.array(time_d.ticks)

    li, ri = find_nearest(times, t1, t2)
    weight_sums = [np.array(weights.data[:,:,x]).sum() for x in range(li, ri)]

    return single_line(times[li:ri], np.array(weight_sums))


def spike_triggered_averages(f, t1, t2, kernel=25, offset=-2):
    """
    Evolution of the sum of weights in time.

    :param f:       NixDumper instance with recorded weights data
    :param t1:      start time (int)
    :param t2:      end time (int)
    :param kernel:  time kernel for the STA (int)
    :param offset:  offset relative to the STA kernel (int)
    """
    block = f.blocks[0]

    input_sources = f.get_neurons_for_layer(block.name, 'input_layer')
    map_sources = f.get_neurons_for_layer(block.name, 'map_layer')

    filt = lambda x: x.type == 'spiketrain' and x.sources[0] in input_sources
    sort_key = lambda x: int(x.sources[0].name)
    input_spiketrains = sorted(filter(filt, block.data_arrays), key=sort_key)

    x_indexes = [int(st.sources[0].name) for st in input_spiketrains]

    values = []
    for nn, neuron in enumerate(map_sources):
        filt = lambda x: x.type == 'spiketrain' and neuron in x.sources
        spiketrain = np.array(filter(filt, block.data_arrays)[0].data[:])

        li, ri = find_nearest(spiketrain, t1, t2)
        spiketrain = spiketrain[li:ri]

        bins = np.array([spiketrain - kernel + offset, spiketrain + offset])

        sta_matrix = np.zeros([len(input_spiketrains), len(spiketrain)])
        for i, st in enumerate(input_spiketrains):
            li, ri = find_nearest(st.data[:], t1, t2)
            data = st.data[li:ri]

            for j in range(bins.shape[-1]):
                sta_matrix[i][j] = ((data >= bins[0][j]) & (data <= bins[1][j])).sum()

        values.append(np.mean(sta_matrix, axis=1))

    title = "Spike triggered averages"
    return multiple_line_plots(np.array(values), x_indexes, title=title)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyse')

    parser.add_argument('--file', type=str, default='sim.h5')

    parser.add_argument('-t1', type=int, default=0)
    parser.add_argument('-t2', type=int, default=-1)

    parser.add_argument('-w, --weights', dest='weights', action='store_true')
    parser.add_argument('-r, --raster', dest='raster', action='store_true')
    parser.add_argument('-v, --voltage', dest='voltage', action='store_true')
    parser.add_argument('-e, --evolution', dest='evo', action='store_true')
    parser.add_argument('-d, --dynamics', dest='dynamics', type=int)

    args = parser.parse_args()

    with NixDumper(args.file, NixDumper.mode['readwrite']) as f:

        s_time = int(args.t1)
        e_time = int(args.t2) if args.t2 > -1 else f.simulation_time

        if args.weights:
            weights_before_and_after(f, t1=s_time, t2=e_time)
        if args.raster:
            raster(f, t1=s_time, t2=e_time)
        if args.voltage:
            time_series(f, t1=s_time, t2=e_time)
        if args.evo:
            weight_sum_evolution(f, t1=s_time, t2=e_time)
        if args.dynamics:
            weight_dynamics_for_single(f, t1=s_time, t2=e_time, target_index=args.dynamics)

    plt.show()

