#!/usr/bin/env python

"""
Creates several plots according to a results of a simulation.

Usage: ./stdp_norm.py [-i <number>] [-r <weight>]

Arguments:
'-i', type=int      number of input neurons
'-w', type=float    weight for all connections, random if -1

Example:

./stdp_norm.py -i 3

"""

import nest
import argparse
import numpy as np
import matplotlib.pyplot as plt

from reduced.simulation.plot.dynamics import *


def inject_current(nest_id, amplitude, start, stop):
    dc = nest.Create("dc_generator")
    nest.SetStatus(dc, [{
        "amplitude": amplitude,
        "start": start,
        "stop": stop
    }])

    nest.Connect(dc, [nest_id])


def execute(neurons_count, conn_weight):
    nest.ResetKernel()

    neuron_setup = {
        'E_L': -65.,
        'C_m': 1.0,
        'tau_m': 20.9,
        't_ref': 2.0,
        'V_th': -50.,
        'V_reset': -55.
    }
    new_neuron = lambda: nest.Create("iaf_psc_alpha", params=neuron_setup)[0]

    # single input neuron
    inputs = [new_neuron() for i in range(neurons_count)]

    # single output neuron
    outputs = [new_neuron()]

    # plastic connection
    synapse_setup = {
        'alpha': 0.1,
        'lambda': 0.01,
        'weight': 0.05,
        'norm_freq': 400.,
        'norm_fac1': 0.9,
        'norm_fac0': 0.2
    }
    nest.CopyModel('stdp_pl_norm_synapse_hom', 'plastic', synapse_setup)

    if conn_weight > 0:
        weights = conn_weight * np.ones(neurons_count)
    else:
        weights = 100.0 * np.random.rand(neurons_count)

    syn_spec = lambda x: {'weight': x, 'model': 'plastic'}
    for input_id, weight in zip(inputs, weights):
        nest.Connect([input_id], outputs, syn_spec=syn_spec(weight))

    connections = nest.GetConnections(inputs, outputs)

    # voltmeters setup
    monitors = []
    rec_params = {'record_from': ['V_m'], 'withtime': True}
    for node in inputs + outputs:
        voltmeter = nest.Create('multimeter', params=rec_params)
        nest.Connect(voltmeter, [node])
        monitors.append(voltmeter[0])

    # simulation
    scales = []
    for t in range(20):  # 10 seconds in total
        state = [nest.GetStatus([synapse_id])[0] for synapse_id in connections]
        scales.append(state)

        amplitude = 10.0 if t < 2 else 1.0
        for i, neuron_id in enumerate(inputs):
            start = t*1000.0 + i*200.0 + 200.0
            stop = start + 50.0 if i < 2 else start + 100.0
            inject_current(neuron_id, amplitude, start, stop)

        nest.Simulate(1000.0)

    print [x['weight'] for x in scales[-1]]

    output = []
    for node_id in monitors:
        output.append(nest.GetStatus([node_id], 'events')[0])

    events = np.array([event['V_m'] for event in output])
    return multiple_time_series(events, output[0]['times'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyse')

    parser.add_argument('-i', type=int, default=3)
    parser.add_argument('-w', type=float, default=10.0)

    args = parser.parse_args()

    execute(args.i, args.w)

    plt.show()