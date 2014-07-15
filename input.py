import itertools
import nest
import nest.topology as tp


INPUT_MOVIE = 'data/gauss20x20.idlmov'



def image_sequence_generator_showcase():

    pre_ISI = 2.0
    post_ISI = 2.5
    stimuli_duration = 20.0
    stimuli_per_object = 5
    nx = 20
    ny = 20
    single_stim_time = stimuli_duration + pre_ISI

    ISG_config = ImageSequenceGeneratorSetup(
        INPUT_MOVIE, stimuli_duration, stimuli_per_object, nx, ny
    )

    nest.ResetKernel()
    img_seq = nest.Create('image_sequence_generator', 1, ISG_config.as_dict)

    nest.Simulate(0.5 * single_stim_time)

    import ipdb
    ipdb.set_trace()

    for i in range(stimuli_per_object):
        frame_num = nest.GetStatus(img_seq, 'current_frame_num')[0]
        nest.Simulate(single_stim_time)



class InputLayer(object):

    def __init__(self, input_weight, ISG_setup, neuron_setup, x_dim=5, y_dim=5):
        """
        Constructor of the input layer. An input layer is a flat layer with
        neurons that fire according to the intensity of the presented images as
         sequence in time. Images are parsed from the given movie file inside
         ImageSequenceGeneratorSetup settings.

        :param input_weight     weight for the connections between the image 
                                generator and the neurons
        :param ISG_setup:       ImageSequenceGeneratorSetup object with image
                                parsing settings
        :param neuron_setup:    NeuronSetup object with settings for the
                                neurons for the input layer
        """
        self._nest_layer = tp.CreateLayer({
            'rows': x_dim,
            'columns': y_dim,
            'elements': neuron_setup.model,
            'edge_wrap': True
        })

        self._nest_nodes = nest.GetNodes(self._nest_layer)[0]
        nest.SetStatus(self._nest_nodes, {"V_m":0.})

        self._movie = nest.Create('image_sequence_generator', 1, ISG_setup.as_dict)
        
        nodes = iter(self._nest_nodes) 
        for x, y in itertools.product(range(x_dim), range(y_dim)):
            node = nodes.next()
            nest.SetStatus([node], {'x': x, 'y': y, 'weight': input_weight})
            nest.Connect(self._movie, [node])

        self._spikes = nest.Create('spike_detector', 1, [{'label': 'input_spikes'}])
        nest.ConvergentConnect(self._nest_nodes, self._spikes)

    @property
    def layer(self):
        return self._nest_layer

    @property
    def nodes(self):
        return self._nest_nodes

    @property
    def spikes(self):
        return self._spikes

    @property
    def movie(self):
        return self._movie

    def clear_spike_detector(self):
        nest.SetStatus(self._spikes, 'n_events', 0)


if __name__=='__main__':
    image_sequence_generator_showcase()
