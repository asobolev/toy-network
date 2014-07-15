import unittest
import nest
import reduced.setup.configurations as CONF
from reduced.input import InputLayer


class TestInputLayer(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

    def test_first_configuration(self):
        self.input_layer = InputLayer(
            200.8, CONF.IMAGE_SEQUENCE_GENERATOR, CONF.INPUT_NEURON
        )

    def tearDown(self):
        pass
