import numpy as np

import nest
import matplotlib.pyplot as plt
import test.configurations as conf
import setup.configurations as base_conf

from nest import raster_plot
from network.layer import InputLayer, MapLayer
from network.connection import ConnectionPool
from reduced.plot import multiple_time_series


def analyse():

    # network setup
    input_layer = InputLayer(
        2000., conf.INPUT['GKLEARN_5X5_0'], conf.NEURONS['INPUT_NEURON']
    )

    map_layer = MapLayer(base_conf.MapNeuron())

    conn_setup = base_conf.ForwardPlasticConnection()
    conn_pool = ConnectionPool(input_layer, map_layer, conn_setup)

    # monitors setup
    monitors = []
    rec_params = {'record_from': ['V_m'], 'withtime': True}
    for node_id in map_layer.nodes:
        voltmeter = nest.Create('multimeter', params=rec_params)
        nest.Connect(voltmeter, [node_id])
        monitors.append(voltmeter[0])
    
    # simulation
    nest.Simulate(2000)
    
    # analysis
    output = []
    for node_id in monitors:
        output.append(nest.GetStatus([node_id], 'events')[0])
    
    events = np.array([event['V_m'] for event in output])
    fig = multiple_time_series(events, output[0]['times'])

    #raster_plot.from_device([input_layer.spikes])
    #raster_plot.from_device([map_layer.spikes])

    plt.show()


if __name__ == '__main__':
    analyse()