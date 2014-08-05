import numpy as np

import nest
import random
import matplotlib.pyplot as plt
import configurations as conf

from nest import raster_plot
from reduced.network.layer import InputLayer, MapLayer
from reduced.network.monitors import VoltageMonitor, MonitorPool
from plot import multiple_time_series, weight_matrix, layer_co_dynamics


def analyse():

    # -------------
    # network setup
    #--------------

    input_layer = InputLayer(2000., conf.GKLEARN_5X5_0_BABY, conf.INPUT_NEURON)

    map_layer = MapLayer(conf.MAP_NEURON, x_dim=5, y_dim=1)

    # plastic connections from input to map layer
    nest.CopyModel('stdp_synapse_hom', 'plastic', {'alpha': 0.1, 'Wmax': 500.})
    targets = [x for x in map_layer]
    params = {
        'delay': 1.0,
        'model': 'plastic',
        }
    for neuron in input_layer:
        weights = [float(x) for x in (50.0 * np.random.rand(len(targets)))]
        #weights = [float(x * 50.0) for x in np.ones(len(targets))]
        neuron.synapse_with(targets, weights, **params)

    # static inhibitory connections in the map layer
    params = {
        'delay': 1.0,
        'model': 'static_synapse',
        }
    for neuron in map_layer:
        neighbors = [x for x in map_layer if not x.id == neuron.id]
        neuron.synapse_with(neighbors, -50.0, **params)

    fig = weight_matrix(input_layer.weights)

    # monitors setup
    input_monitors = MonitorPool(VoltageMonitor, input_layer.nodes)
    map_monitors = MonitorPool(VoltageMonitor, map_layer.nodes)

    # ----------
    # simulation
    #-----------

    # simulation
    nest.Simulate(10000)

    #weight_means_before = np.array([x.mean() for x in input_layer.weights])
    #weight_means_after = np.array([x.mean() for x in input_layer.weights])
    #weight_means_diff = weight_means_after - weight_means_before

    #for neuron in input_layer:
    #    nest.SetStatus([neuron.id], 'weight', 0.1)

    # analysis
    events_i = np.array([vm.V_m for vm in input_monitors])
    events_m = np.array([vm.V_m for vm in map_monitors])

    #layer_co_dynamics(events_i, events_m, input_monitors[0].times)

    #raster_plot.from_device([input_layer.spikes])
    #raster_plot.from_device([map_layer.spikes])

    fig = weight_matrix(input_layer.weights)
    #fig = weight_matrix(map_layer.weights)

    plt.show()


if __name__ == '__main__':
    analyse()
