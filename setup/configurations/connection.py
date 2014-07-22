from reduced.setup.models import *


class ForwardStaticConnection(ConnectionSetup):

    synapse_model = 'static_synapse'
    connection_type = 'convergent'
    mask = {
        'circular': {'radius': 0.2}
    }
    weights = {
        'gaussian': {
            'p_center': 2.0,
            'sigma': 0.10
        }
    }


class ForwardPlasticConnection(ConnectionSetup):

    synapse_model = 'stdp_pl_norm_synapse_hom'
    connection_type = 'convergent'
    weights = {'uniform': {'min': 1., 'max': 200.}}


class PlasticSynapse(SynapseSetup):

    alpha = 0.1
    lambda_ = 0.01
    weight = 0.05
    norm_freq = 400.
    norm_fac1 = 0.9
    norm_fac0 = 0.2