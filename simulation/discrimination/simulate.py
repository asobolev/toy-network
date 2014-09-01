#!/usr/bin/env python

"""
This script is aimed to build a network according to the given configuration
and record the evolution of weights between input and map layer neurons. It
runs the simulation in steps and records weights after every phase. The
simulation results are stored in an HDF5 file (NIX format).

Example:

./simulate.py -t 20000 -p 1000 -c "config/01.json"

"""

import nest
import argparse
import numpy as np

from reduced.simulation.utils import *
from reduced.setup import *
from reduced.network.layer import InputLayer, MapLayer
from reduced.network.monitors import SpikeDetector, VoltageMonitor, MonitorPool
from reduced.simulation.dump import NixDumper


def simulate(simulation_time, phase, config_path, output_path):
    nest.ResetKernel()
    setup_dict = from_file(config_path)  # network configuration

    #--------------
    # Network setup
    #--------------

    # input layer
    input_setup = ISGStraightSetup(**setup_dict['STIMULI'])
    neuron_setup = NeuronSetup(**setup_dict['INPUT_NEURON'])
    dimensions = setup_dict['INPUT_LAYER']
    input_layer = InputLayer(input_setup, neuron_setup, **dimensions)
    
    # output layer
    neuron_setup = NeuronSetup(**setup_dict['MAP_NEURON'])
    dimensions = setup_dict['MAP_LAYER']
    map_layer = MapLayer(neuron_setup, **dimensions)

    # connections from input to map layer
    synapse_setup = SynapseHomNormSetup(**setup_dict['SYNAPSE'])
    conn_setup = ConnectionSetup(**setup_dict['FWD_CONN'])
    nest.CopyModel(conn_setup.model, 'plastic', synapse_setup.as_nest_dict)

    wc = conn_setup.weight_coeff
    for neuron in input_layer:
        weights = list(wc * np.random.rand(len(map_layer)))
        neuron.synapse_with(map_layer, weights, model='plastic')

    #--------------
    # Devices setup
    #--------------

    time_passed = 0

    spike_detector_i = SpikeDetector(input_layer.nodes)
    spike_detector_m = SpikeDetector(map_layer.nodes)
    input_monitors = MonitorPool(VoltageMonitor, input_layer.nodes)
    map_monitors = MonitorPool(VoltageMonitor, map_layer.nodes)
    spider = []  # collector for actual synaptic states (weights)
    syn_times = []   # records times when states were collected

    get_as_dict = lambda synapses: [x.as_dict() for x in synapses]

    #------------------------------
    # Simulate with cycles == phase
    #------------------------------

    while time_passed < simulation_time:
        spider.append(get_as_dict(input_layer.synapses))
        syn_times.append(time_passed)

        nest.Simulate(phase)
        time_passed += phase

    #-------------------
    # Dump synaptic data
    #-------------------

    block_name = 'simulation'
    stimuli_duration = input_setup.stimuli_duration

    with NixDumper(output_path, NixDumper.mode['overwrite']) as nd:
        nd.create_block(block_name, time_passed, input_layer, map_layer)

        # create stimulus
        positions = [phase * i for i in range(int(time_passed / phase))]
        extents = [stimuli_duration for i in range(len(positions))]
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
        for m in list(input_monitors) + list(map_monitors):
            nd.dump_analogsignal(block_name, m.observable, m.times, m.V_m)

        # dump synapses
        synapse_sample = spider[0]

        sources = np.array(sorted(set([int(x['source']) for x in synapse_sample])))
        targets = np.array(sorted(set([int(x['target']) for x in synapse_sample])))
        times = np.array(syn_times)

        weight_matrix = np.zeros((len(sources), len(targets), len(times)))
        for t, snapshot in enumerate(spider):
            for synapse in snapshot:
                i = np.where(sources == int(synapse['source']))[0][0]
                j = np.where(targets == int(synapse['target']))[0][0]
                weight_matrix[i][j][t] = synapse['weight']

        nd.dump_weights(block_name, sources, targets, times, weight_matrix)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulation')

    parser.add_argument('-t, --time', dest='time', type=int)
    parser.add_argument('-p, --phase', dest='phase', type=int)
    parser.add_argument('-c, --conf', dest='conf', type=str, default='config/01.json')
    parser.add_argument('-o, --output', dest='output', type=str, default='sim.h5')

    args = parser.parse_args()
    assert(args.time >= args.phase)

    simulate(args.time, args.phase, args.conf, args.output)