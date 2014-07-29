import numpy as np

import nest
import matplotlib.pyplot as plt
import configurations as conf

from nest import raster_plot
from reduced.network.layer import InputLayer, MapLayer
from plot import multiple_time_series, weight_matrix, layer_co_dynamics

def set_voltage_monitors(nest_node_ids):
    def create_voltmeter(node_id):
        voltmeter = nest.Create('multimeter', params=rec_params)
        nest.Connect(voltmeter, [node_id])
        return voltmeter[0]

    rec_params = {'record_from': ['V_m'], 'withtime': True}
    return map(create_voltmeter, nest_node_ids)


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
    input_monitors = set_voltage_monitors(input_layer.nodes)
    map_monitors = set_voltage_monitors(map_layer.nodes)

    #weight_means_before = np.array([x.mean() for x in input_layer.weights])
    
    # simulation
    nest.Simulate(5000)

    #weight_means_after = np.array([x.mean() for x in input_layer.weights])
    #weight_means_diff = weight_means_after - weight_means_before

    #print weight_means_diff

    #for neuron in input_layer:
    #    nest.SetStatus([neuron.id], 'weight', 0.1)

    # analysis
    output_i = []
    for node_id in input_monitors:
        output_i.append(nest.GetStatus([node_id], 'events')[0])

    output_m = []
    for node_id in map_monitors:
        output_m.append(nest.GetStatus([node_id], 'events')[0])
    
    events_i = np.array([event['V_m'] for event in output_i])
    events_m = np.array([event['V_m'] for event in output_m])
    #fig = multiple_time_series(events, output[0]['times'])

    layer_co_dynamics(events_i, events_m, output_i[0]['times'])

    #raster_plot.from_device([input_layer.spikes])
    #raster_plot.from_device([map_layer.spikes])

    fig = weight_matrix(input_layer.weights_normalized)

    plt.show()


if __name__ == '__main__':
    analyse()
