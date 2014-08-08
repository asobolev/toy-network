import unittest
import numpy as np

import nest

import configurations as conf
from reduced.network.layer import InputLayer


class TestInputLayer(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

    def test_spiking(self):
        conf_dict = {
            'input_weight': 2000.,
            'ISG_setup': conf.GKLEARN_5X5_0,
            'neuron_setup': conf.INPUT_NEURON,
            'x_dim': 5,
            'y_dim': 5
        }
        self.input_layer = InputLayer(**conf_dict)

        nest.Simulate(2000)

        events = nest.GetStatus([self.input_layer.spikes], 'events')[0]
        senders = events['senders']

        has_spikes = lambda node_id: np.sum(senders == node_id) > 2
        spiking_nodes = [x for x in self.input_layer.nodes if has_spikes(x)]
        silent_nodes = [x for x in self.input_layer.nodes if not has_spikes(x)]

        assert(len(spiking_nodes) == 20)
        assert(len(silent_nodes) == 5)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()