import numpy as np

import nest
import random
import matplotlib.pyplot as plt
import configurations as conf

from nest import raster_plot
from reduced.network.layer import InputLayer, MapLayer
from reduced.network.monitors import VoltageMonitor, MonitorPool
from plot.dynamics import multiple_time_series, layer_co_dynamics
from plot.weights import weights_multiple, neuron_ids_in_layer


def network_setup():
    input_layer = InputLayer(2000., conf.GKLEARN_5X5_0_BABY, conf.INPUT_NEURON)

    map_layer = MapLayer(conf.MAP_NEURON)

    # plastic connections from input to map layer
    nest.CopyModel('stdp_synapse_hom', 'plastic', {'alpha': 0.1, 'Wmax': 500.})
    targets = [x for x in map_layer]
    params = {
        'delay': 1.0,
        'model': 'plastic',
    }
    for neuron in input_layer:
        weights = [float(x) for x in (100.0 * np.random.rand(len(targets)))]
        neuron.synapse_with(targets, weights, **params)

    # static random inhibitory connections in the map layer
    params = {
        'delay': 1.0,
        'model': 'static_synapse',
    }
    for neuron in map_layer:
        some = random.sample(map_layer, 12)  # may include itself
        neuron.synapse_with(some, -250.0, **params)

    # excitatory connections to neighboring neurons
    params = {
        'delay': 1.0,
        'model': 'static_synapse',
    }
    #for column in in map_layer.as_matrix:
    #    some = random.sample(map_layer, 12)
    #    neuron.synapse_with(some, -250.0, **params)


    return input_layer, map_layer


def simulation(input_layer, map_layer):

    # save weights
    weights_before = np.array(input_layer.weights)

    # monitors setup
    input_monitors = MonitorPool(VoltageMonitor, input_layer.nodes)
    map_monitors = MonitorPool(VoltageMonitor, map_layer.nodes)

    # ----------
    # simulation
    #-----------
    
    # simulation
    nest.Simulate(10000)

    weights_after = np.array(input_layer.weights)

    #weight_means_before = np.array([x.mean() for x in input_layer.weights])
    #weight_means_after = np.array([x.mean() for x in input_layer.weights])
    #weight_means_diff = weight_means_after - weight_means_before

    #for neuron in input_layer:
    #    nest.SetStatus([neuron.id], 'weight', 0.1)

    # simulation
    events_i = np.array([vm.V_m for vm in input_monitors])
    events_m = np.array([vm.V_m for vm in map_monitors])

    #layer_co_dynamics(events_i, events_m, input_monitors[0].times)

    #raster_plot.from_device([input_layer.spikes])
    #raster_plot.from_device([map_layer.spikes], hist=True)

    fig = neuron_ids_in_layer(map_layer)

    #fig = weights_multiple([weights_before, weights_after])

    plt.show()


if __name__ == '__main__':
    input_layer, map_layer = network_setup()
    simulation(input_layer, map_layer)
