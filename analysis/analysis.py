import numpy as np

import nest
import matplotlib.pyplot as plt
import configurations as conf

from nest import raster_plot
from reduced.network.layer import InputLayer, MapLayer
from reduced.network.monitors import VoltageMonitor, MonitorPool
from plot import multiple_time_series, weight_matrix, layer_co_dynamics


def analyse():

    # network setup
    args = [2000., conf.INPUT['GKLEARN_5X5_0'], conf.NEURONS['INPUT_NEURON']]
    input_layer = InputLayer(*args)

    map_layer = MapLayer(conf.NEURONS['MAP_NEURON'])


    nest.CopyModel('stdp_synapse_hom', 'plastic', {'alpha': 0.1, 'Wmax': 1000.})
    targets = [x for x in map_layer]
    params = {
        'delay': 1.0,
        'model': 'plastic',
    }
    for neuron in input_layer:
        weights = [float(x) for x in (300.0 * np.random.rand(len(targets)))]
        neuron.synapse_with(targets, weights, **params)

    # monitors setup
    input_monitors = MonitorPool(VoltageMonitor, input_layer.nodes)
    map_monitors = MonitorPool(VoltageMonitor, map_layer.nodes)

    #weight_means_before = np.array([x.mean() for x in input_layer.weights])
    
    # simulation
    nest.Simulate(5000)

    #weight_means_after = np.array([x.mean() for x in input_layer.weights])
    #weight_means_diff = weight_means_after - weight_means_before

    #for neuron in input_layer:
    #    nest.SetStatus([neuron.id], 'weight', 0.1)

    # analysis
    events_i = np.array([vm.V_m for vm in input_monitors])
    events_m = np.array([vm.V_m for vm in map_monitors])

    layer_co_dynamics(events_i, events_m, input_monitors[0].times)

    #raster_plot.from_device([input_layer.spikes])
    #raster_plot.from_device([map_layer.spikes])

    fig = weight_matrix(input_layer.weights_normalized)

    plt.show()


if __name__ == '__main__':
    analyse()
