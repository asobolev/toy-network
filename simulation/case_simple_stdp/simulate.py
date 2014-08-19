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
from reduced.simulation.dump import Dumper


def simulate(simulation_time, config_path, output_path):

    #--------------
    # Network setup
    #--------------

    nest.ResetKernel()

    setup_dict = parse_to_objects(from_file(config_path))

    network_setup = [
        setup_dict['GKLEARN_5X5_0'], setup_dict['INPUT_NEURON'],
        setup_dict['MAP_NEURON'], setup_dict['HOM_SYNAPSE'],
        setup_dict['FWD_CONN'], setup_dict['INH_CONN'],
        setup_dict.get('EXC_CONN', None)
    ]
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
    times = []   # records times when states were collected

    get_as_dict = lambda synapses: [x.as_dict() for x in synapses]

    #--------------------------------------------------------
    # Simulate with cycles equal to one stimulus presentation
    #--------------------------------------------------------

    while time_passed < simulation_time:
        nest.Simulate(phase)
        time_passed += phase

        spider.append(get_as_dict(network.input_layer.synapses))
        times.append(time_passed)

    #-------------------
    # Dump synaptic data
    #-------------------

    dumper = Dumper(output_path, 'w')

    dumper.dump_input_spikes(spike_detector_i.times, spike_detector_i.senders)

    dumper.dump_map_spikes(spike_detector_m.times, spike_detector_m.senders)

    dumper.dump_synapse_snapshots(times, spider)

    dump_voltage = lambda m: dumper.dump_voltage_trace(m.observable, m.times, m.V_m)
    map(dump_voltage, map_monitors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulation')

    parser.add_argument('-t, --time', dest='time', type=int)
    parser.add_argument('-c, --conf', dest='conf', type=str, default='configuration/01.json')
    parser.add_argument('-o, --output', dest='output', type=str, default='weights.h5')

    args = parser.parse_args()
    simulate(args.time, args.conf, args.output)