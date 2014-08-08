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