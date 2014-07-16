import unittest
import nest
from nest import raster_plot, voltage_trace
import reduced.setup.configurations as CONF
from reduced.input import InputLayer


class TestInputLayer(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

    def test_first_configuration(self):
        self.input_layer = InputLayer(
            200.8, CONF.IMAGE_SEQUENCE_GENERATOR_5X5, CONF.INPUT_NEURON
        )

        voltmeter = nest.Create("voltmeter")
        nest.SetStatus(voltmeter, [{"withtime": True}])
        nest.Connect(voltmeter, [self.input_layer.nodes[15]])

        # simulation
        nest.Simulate(2000)

        # analysis
        nest.GetStatus(voltmeter, 'events')

        import ipdb
        ipdb.set_trace()

        voltage_trace.from_device(voltmeter)
        voltage_trace.show()

        #raster_plot.from_device(self.input_layer.spikes)
        #raster_plot.show()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()