from __future__ import absolute_import
from reduced.setup.base import SetupBase


class ConnectionSetup(SetupBase):

    model = None

    @property
    def is_valid(self):
        return self.model is not None


class ForwardConnectionSetup(SetupBase):

    model = None
    wmax = None


class InhibitoryConnectionSetup(SetupBase):

    model = None
    quantity = None
    weight = None


class ExcitatoryConnectionSetup(SetupBase):

    model = None
    weight = None