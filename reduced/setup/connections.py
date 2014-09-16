from __future__ import absolute_import
from reduced.setup.base import SetupBase


class ConnectionSetup(SetupBase):

    model = None
    weight_coeff = None
    quantity = None

    @property
    def is_valid(self):
        return self.model is not None