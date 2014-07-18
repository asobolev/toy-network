import unittest
import nest
import numpy as np
import configurations as conf
import matplotlib.pyplot as plt

from nest import raster_plot
from reduced.input import InputLayer
from reduced.plot import multiple_time_series


class TestInputLayer(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

    def test_first_configuration(self):
        self.input_layer = InputLayer(
            2000., conf.INPUT['GKLEARN_5X5_0'], conf.NEURONS['INPUT_NEURON']
        )

        monitors = []
        rec_params = {'record_from': ['V_m'], 'withtime': True}
        for node_id in self.input_layer.nodes:
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
        #fig = multiple_time_series(events, output[0]['times'])

        #plt.show()

        raster_plot.from_device(self.input_layer.spikes)
        raster_plot.show()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()