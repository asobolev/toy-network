from collections import namedtuple


tuple_NeuronSetup = namedtuple(
    'tuple_NeuronSetup',
    ['model', 'para_dict', 'noise_firing_rate', 'noise_amplitude',
     'lat_ex_input_ports']
)
class NeuronSetup(tuple_NeuronSetup):

    @property
    def noise_parameters(self):
        return {
            'p_rate': self.noise_firing_rate,
            'amplitude': self.noise_amplitude
        }

    @property
    def as_dict(self):
        return {
            'model': self.model,
            'para_dict': self.para_dict,
            'noise_paras': self.noise_parameters,
            'lat_ex_input_ports': self.lat_ex_input_ports
        }


tuple_ImageSequenceGeneratorSetup = namedtuple(
    'tuple_ImageSequenceGeneratorSetup',
    ['movie_path', 'stimuli_duration', 'stimuli_per_object', 'nx', 'ny',
     'pre_ISI', 'post_ISI', 'type', 'stim_direction']
)
class ImageSequenceGeneratorSetup(tuple_ImageSequenceGeneratorSetup):

    @property
    def _player_parameters(self):
        return {
            'stimulus_interval': self.stimuli_duration,
            'inter_stimulus_interval': self.pre_ISI,
            'inter_stimulus_interval2': self.post_ISI,
            'stimuli_per_object': self.stimuli_per_object,
            'nx': self.nx,
            'ny': self.ny,
            'stim_direction': self.stim_direction
        }

    @property
    def _player(self):
        return {
            'type': self.type,
            'parameter': self._player_parameters
        }

    @property
    def as_dict(self):
        return {
            'filename': self.movie_path,
            'player': self._player
        }