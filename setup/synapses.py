from __future__ import absolute_import
from reduced.setup.base import SetupBase


class SynapseSetup(SetupBase):

    # an abstract class for synapse setup

    tau_plus = None
    alpha = None
    lambda_ = None

    @property
    def is_valid(self):
        return self.alpha is not None


class SynapseHomNormSetup(SynapseSetup):

    weight = None
    norm_freq = None
    norm_fac1 = None
    norm_fac0 = None

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


class SynapseHomSetup(SynapseSetup):

    mu_plus = None
    mu_minus = None
    Wmax = None

    @property
    def as_nest_dict(self):
        attrs = ('tau_plus', 'alpha', 'mu_plus', 'mu_minus', 'Wmax')
        combined = zip(attrs, map(lambda x: getattr(self, x), attrs))
        not_none = filter(lambda x: x[1] is not None, combined)

        if self.lambda_ is not None:
            not_none.append(('lambda', self.lambda_))

        return dict(not_none)
