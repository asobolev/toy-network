#!/usr/bin/env python

"""
This script is aimed to record the evolution of weights between input and map
layer neurons. It runs the simulation in small time steps and records weights
after every stimulus presentation.

Example:

./simulate.py -t 20000 -c "configuration/02.json"

"""

import nest
import argparse
import numpy as np

from reduced.network.network import ToyNetwork
from reduced.network.monitors import SpikeDetector, VoltageMonitor, MonitorPool
from reduced.simulation.utils import *
from reduced.simulation.dump import NixDumper


def simulate(simulation_time, config_path, output_path):

    #--------------
    # Network setup
    #--------------

    nest.ResetKernel()

    setup_dict = parse_to_objects(from_file(config_path))

    param_names = ['GKLEARN_5X5_0', 'INPUT_NEURON', 'MAP_NEURON', 'HOM_SYNAPSE',
                   'FWD_CONN', 'INH_CONN', 'EXC_CONN']

    network_setup = [setup_dict.get(x, None) for x in param_names]
    network = ToyNetwork(*network_setup)

    #---------
    # Learning
    #---------

    i_s_i = setup_dict['GKLEARN_5X5_0'].i_s_i
    stimuli_duration = setup_dict['GKLEARN_5X5_0'].stimuli_duration
    phase = + i_s_i + stimuli_duration
    time_passed = 0

    spike_detector_i = SpikeDetector(network.input_layer.nodes)
    spike_detector_m = SpikeDetector(network.map_layer.nodes)
    map_monitors = MonitorPool(VoltageMonitor, network.map_layer.nodes)
    spider = []  # collector for actual synaptic states (weights)
    syn_times = []   # records times when states were collected

    get_as_dict = lambda synapses: [x.as_dict() for x in synapses]

    #--------------------------------------------------------
    # Simulate with cycles equal to one stimulus presentation
    #--------------------------------------------------------

    while time_passed < simulation_time:
        nest.Simulate(phase)
        time_passed += phase

        spider.append(get_as_dict(network.input_layer.synapses))
        syn_times.append(time_passed)

    #-------------------
    # Dump synaptic data
    #-------------------

    block_name = 'simulation'
    with NixDumper(output_path, NixDumper.mode['overwrite']) as nd:
        nd.create_block(block_name, network.input_layer, network.map_layer)

        # create stimulus
        positions = [phase * i for i in range(int(time_passed / phase))]
        extents = [i_s_i for i in range(len(positions))]
        stimulus = [float(i % 4) + 1 for i in range(len(positions))]

        nd.dump_stimulus(block_name, positions, extents, stimulus)

        # dump spike events
        def dump_spikes(events, senders):
            neuron_ids = set(senders)
            for nest_id in neuron_ids:
                indexes = np.where(senders == nest_id)
                nd.dump_spiketrain(block_name, nest_id, events[indexes])

        dump_spikes(spike_detector_i.times, spike_detector_i.senders)
        dump_spikes(spike_detector_m.times, spike_detector_m.senders)

        # dump voltage traces
        for m in map_monitors:
            nd.dump_analogsignal(block_name, m.observable, m.times, m.V_m)

        # dump synapses
        synapse_sample = spider[0]
        synapse_ids = [(x['source'], x['target']) for x in synapse_sample]

        times = np.array(syn_times)
        weights = np.array([[x['weight'] for x in synapses] for synapses in spider])

        for i, id_pair in enumerate(synapse_ids):
            source, target = id_pair  # source, target are NEST ids

            data = [x[i] for x in weights]
            nd.dump_synapse(block_name, source, target, times, data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulation')

    parser.add_argument('-t, --time', dest='time', type=int)
    parser.add_argument('-c, --conf', dest='conf', type=str, default='configuration/01.json')
    parser.add_argument('-o, --output', dest='output', type=str, default='weights.h5')

    args = parser.parse_args()
    simulate(args.time, args.conf, args.output)