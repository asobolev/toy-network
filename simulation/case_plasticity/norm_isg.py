#!/usr/bin/env python

"""
Creates several plots according to a results of a simulation.

Usage: ./stdp_norm.py [-r <weight>]

Arguments:
'-w', type=float    weight for all connections, random if -1

Example:

./stdp_norm.py -w 3.0

"""

import nest
import argparse
import numpy as np
import matplotlib.pyplot as plt

from reduced.setup.inputs import ISGStraightSetup
from reduced.setup.neurons import NeuronSetup
from reduced.network.layer import InputLayer
from reduced.simulation.plot.dynamics import *


def inject_current(nest_id, amplitude, start, stop):
    dc = nest.Create("dc_generator")
    nest.SetStatus(dc, [{
        "amplitude": amplitude,
        "start": start,
        "stop": stop
    }])

    nest.Connect(dc, [nest_id])


def execute(conn_weight):
    nest.ResetKernel()

    # 5x5 input layer
    input_setup = ISGStraightSetup(**{
        "stimuli_duration": 200.0,
        "i_s_i": 50.0,
        "movie_path": "../../data/5x5gklearn0.idlmov"
    })
    neuron_setup = NeuronSetup(**{
        "model": "pixel_iaf_psc_exp",
        "para_dict": {},
        "lat_ex_input_ports": [],
        "noise_firing_rate": 12000.0,
        "noise_amplitude": 13.9
    })
    input_layer = InputLayer(2000.0, input_setup, neuron_setup, x_dim=3, y_dim=3)
    
    # single output neuron
    neuron_setup = NeuronSetup(**{
        "model": "iaf_psc_alpha",
        "para_dict": {
            "E_L": -65.0,
            "C_m": 1.0,
            "tau_m": 20.9,
            "t_ref": 2.0,
            "V_th": -50.0,
            "V_reset": -55.0
        }
    })
    output_id = nest.Create(neuron_setup.model, params=neuron_setup.para_dict)[0]

    inputs = input_layer.nodes
    outputs = [output_id]

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

    weights = 20.0 * np.random.rand(len(inputs))

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
    for t in range(50):
        state = [nest.GetStatus([synapse_id])[0] for synapse_id in connections]
        scales.append(state)

        start, stop = 0.0, 0.0
        for i, neuron_id in enumerate(inputs):
            if i % 3 == 0:
                start = t*1000.0 + int(i/3)*200.0 + 200.0
                stop = start + 100.0 #if i < 2*3 else start + 100.0
            inject_current(neuron_id, 2.0, start, stop)

        nest.Simulate(1000.0)

    print [x['weight'] for x in scales[-1]]

    output = []
    for node_id in monitors:
        output.append(nest.GetStatus([node_id], 'events')[0])

    events = np.array([event['V_m'] for event in output])
    return multiple_time_series(events, output[0]['times'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyse')

    parser.add_argument('-w', type=float, default=10.0)

    args = parser.parse_args()

    execute(args.w)

    plt.show()
