from __future__ import absolute_import
from reduced.setup.base import SetupBase


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