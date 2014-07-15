import unittest
import nest
import nest.raster_plot as raster_plot
import reduced.setup.configurations as CONF
from reduced.input import InputLayer


class TestInputLayer(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

    def test_first_configuration(self):
        self.input_layer = InputLayer(
            200.8, CONF.IMAGE_SEQUENCE_GENERATOR, CONF.INPUT_NEURON
        )

        nest.Simulate(2000)

        raster_plot.from_device(self.input_layer.spikes)
        raster_plot.show()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()