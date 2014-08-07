import numpy as np

import nest
import random
import itertools as it
import matplotlib.pyplot as plt
import configurations as conf

from nest import raster_plot
from reduced.network.layer import InputLayer, MapLayer
from reduced.network.monitors import VoltageMonitor, MonitorPool
from plot.dynamics import multiple_time_series, layer_co_dynamics
from plot.weights import weights_multiple, neuron_ids_in_layer


def network_setup():

    input_layer = InputLayer(2000., conf.GKLEARN_5X5_0, conf.INPUT_NEURON)
    map_layer = MapLayer(conf.MAP_NEURON)

    # plastic connections from input to map layer
    nest.CopyModel('stdp_synapse_hom', 'plastic', 
                   conf.HOM_SYNAPSE.as_nest_dict)
    nest.CopyModel('stdp_pl_norm_synapse_hom', 'plastic_normalized',
                   conf.HOM_NORM_SYNAPSE.as_nest_dict)

    targets = [x for x in map_layer]
    for neuron in input_layer:
        weights = [float(x) for x in (100.0 * np.random.rand(len(targets)))]
        neuron.synapse_with(targets, weights, model='plastic')

    # static random inhibitory connections in the map layer
    for neuron in map_layer:
        some = random.sample(map_layer, 12)  # may include itself
        neuron.synapse_with(some, -500.0, model='static_synapse')

    # excitatory connections to neighboring neurons
    for x, row in enumerate(map_layer.as_matrix):
        for y, neuron in enumerate(row):
            horizontal = (x-1, x, x+1 if x+1 < map_layer.x_dim else -1)
            vertical = (y-1, y, y+1 if y+1 < map_layer.y_dim else -1)
            coords = it.product(horizontal, vertical)
            coords = filter(lambda q: not q == (x, y), coords)

            neighbors = [map_layer.as_matrix[i][j] for i, j in coords]
            neuron.synapse_with(neighbors, 250.0, model='static_synapse')

    return input_layer, map_layer


def simulation(input_layer, map_layer):

    # monitors setup
    weights_before = np.array(input_layer.weights)
    input_monitors = MonitorPool(VoltageMonitor, input_layer.nodes)
    map_monitors = MonitorPool(VoltageMonitor, map_layer.nodes)

    # simulation
    nest.Simulate(10000)

    # resulting data
    weights_after = np.array(input_layer.weights)
    events_i = np.array([vm.V_m for vm in input_monitors])
    events_m = np.array([vm.V_m for vm in map_monitors])

    # --------
    # analysis
    # --------

    # compare voltage outputs
    layer_co_dynamics(events_i, events_m, input_monitors[0].times)

    # spike raster plots
    #raster_plot.from_device([input_layer.spikes])
    raster_plot.from_device([map_layer.spikes], hist=True)

    # output neuron IDs as a colored matrix
    #fig = neuron_ids_in_layer(map_layer)

    # weights before and after
    fig = weights_multiple([weights_before, weights_after])

    plt.show()


if __name__ == '__main__':
    input_layer, map_layer = network_setup()
    simulation(input_layer, map_layer)

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
