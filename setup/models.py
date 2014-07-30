from __future__ import absolute_import


class SetupBase(object):
    """
    A Base abstract class to describe setups for different object types, like
    Neurons, Connections, Input devices etc.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def is_valid(self):
        raise NotImplementedError()

    @property
    def as_nest_dict(self):
        raise NotImplementedError()


class NeuronSetup(SetupBase):

    model = None
    para_dict = {}
    noise_firing_rate = None
    noise_amplitude = None
    lat_ex_input_ports = None

    @property
    def is_valid(self):
        return self.model is not None

    @property
    def as_nest_dict(self):
        return {
            'model': self.model,
            'para_dict': self.para_dict,
            'noise_paras': {
                'p_rate': self.noise_firing_rate,
                'amplitude': self.noise_amplitude
            },
            'lat_ex_input_ports': self.lat_ex_input_ports
        }


class ISGStraightSetup(SetupBase):

    movie_path = None
    stimuli_duration = None
    i_s_i = None

    @property
    def is_valid(self):
        not_none = lambda x, y: x and (getattr(self, y) is not None)
        return reduce(not_none, ['movie_path', 'stimuli_duration', 'i_s_i'], True)

    @property
    def as_nest_dict(self):
        return {
            'filename': self.movie_path,
            'player': {
                'type': 'straight',
                'parameter': {
                    'stimulus_interval': self.stimuli_duration,
                    'inter_stimulus_interval': self.i_s_i,
                }
            }
        }


class ISGSequenceSetup(SetupBase):

    movie_path = None
    stimuli_duration = None
    stimuli_per_object = None
    nx = None
    ny = None
    i_s_i = None
    i_s_i_2 = None
    stim_direction = 'x_continuous'

    @property
    def is_valid(self):
        not_none = lambda x, y: x and (getattr(self, y) is not None)
        attrs_to_validate = ['movie_path', 'stimuli_duration',
                             'stimuli_per_object', 'i_s_i', 'nx', 'ny']
        return reduce(not_none, attrs_to_validate, True)

    @property
    def as_nest_dict(self):
        return {
            'filename': self.movie_path,
            'player': {
                'type': 'xysequence',
                'parameter': {
                    'stimulus_interval': self.stimuli_duration,
                    'inter_stimulus_interval': self.i_s_i,
                    'inter_stimulus_interval2': self.i_s_i_2,
                    'stimuli_per_object': self.stimuli_per_object,
                    'nx': self.nx,
                    'ny': self.ny,
                    'stim_direction': self.stim_direction
                }
            }
        }


class ConnectionSetup(SetupBase):

    synapse_model = None
    connection_type = None
    mask = None
    weights = None

    @property
    def is_valid(self):
        not_none = lambda x, y: x and (getattr(self, y) is not None)
        return reduce(not_none, ['synapse_model', 'connection_type'], True)

    @property
    def as_nest_dict(self):
        result = {
            'synapse_model': self.synapse_model,
            'connection_type': self.connection_type
        }
        if self.mask is not None:
            result['mask'] = self.mask
        if self.weights is not None:
            result['weights'] = self.weights
        return result


class SynapseSetup(SetupBase):

    alpha = None
    lambda_ = None
    weight = None
    norm_freq = None
    norm_fac1 = None
    norm_fac0 = None

    @property
    def is_valid(self):
        not_none = lambda x, y: x and (getattr(self, y) is not None)
        return reduce(not_none, ['alpha', 'lambda_', 'weight'], True)

    @property
    def as_nest_dict(self):
        return {
            'alpha': self.alpha,
            'lambda': self.lambda_,
            'weight': self.weight,
            'norm_freq': self.norm_freq,
            'norm_fac1': self.norm_fac1,
            'norm_fac0': self.norm_fac0,
        }
