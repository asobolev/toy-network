import numpy as np

import nest
import matplotlib.pyplot as plt
from nest import raster_plot

from reduced.network.network import ToyNetwork
from reduced.network.monitors import VoltageMonitor, MonitorPool
from reduced.simulation.utils import from_file, parse_to_objects
from reduced.simulation.plot.dynamics import layer_co_dynamics
from reduced.simulation.plot.weights import weights_multiple


def simulation(network):

    # monitors setup
    weights_before = np.array(network.input_layer.weights)
    input_monitors = MonitorPool(VoltageMonitor, network.input_layer.nodes)
    map_monitors = MonitorPool(VoltageMonitor, network.map_layer.nodes)

    # simulation
    nest.Simulate(10000)

    # resulting data
    weights_after = np.array(network.input_layer.weights)
    events_i = np.array([vm.V_m for vm in input_monitors])
    events_m = np.array([vm.V_m for vm in map_monitors])

    # --------
    # analysis
    # --------

    # compare voltage outputs
    layer_co_dynamics(events_i, events_m, input_monitors[0].times)

    # spike raster plots
    #raster_plot.from_device([network.input_layer.spikes])
    raster_plot.from_device([network.map_layer.spikes], hist=True)

    # output neuron IDs as a colored matrix
    #fig = neuron_ids_in_layer(network.map_layer)

    # weights before and after
    fig = weights_multiple([weights_before, weights_after])

    plt.show()


if __name__ == '__main__':

    setup_dict = parse_to_objects(from_file('configurations.json'))

    network_setup = [
        setup_dict['GKLEARN_5X5_0'], setup_dict['INPUT_NEURON'],
        setup_dict['MAP_NEURON'], setup_dict['HOM_SYNAPSE'],
        setup_dict['FWD_CONN'], setup_dict['INH_CONN'], setup_dict['EXC_CONN']
    ]
    network = ToyNetwork(*network_setup)

    simulation(network)

    """
    Some potentially useful techniques:

    # weight means analysis
    weight_means_before = np.array([x.mean() for x in input_layer.weights])
    weight_means_after = np.array([x.mean() for x in input_layer.weights])
    weight_means_diff = weight_means_after - weight_means_before

    # reset of the input layer weights
    for neuron in input_layer:
        nest.SetStatus([neuron.id], 'weight', 0.1)
    """
