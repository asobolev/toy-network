from __future__ import absolute_import
from reduced.setup.base import SetupBase


class ISGStraightSetup(SetupBase):

    weight = 2000.0
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