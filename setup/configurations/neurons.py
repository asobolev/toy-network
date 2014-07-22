from reduced.setup.models import *


class MapNeuron(NeuronSetup):

    model = 'iaf_psc_alpha'
    para_dict = {
        'C_m': 1.0,
        'tau_m': 20.9,
        't_ref': 2.0,
        'E_L': 0.0,
        'V_th': 20.,
        'V_reset': 10.
    }
    lat_ex_input_ports = [0]


class InputNeuron(NeuronSetup):

    model = 'pixel_iaf_psc_exp'
    para_dict = {}
    lat_ex_input_ports = []
    noise_firing_rate = 12000.
    noise_amplitude = 13.9  # 3 Hz background noise


class ExcitatoryNeuron(NeuronSetup):

    model = 'iaf_cond_diffexp_ang'
    para_dict = {
        'V_th': -50.0,
        'V_reset': -55.0,
        't_ref': 1.0,
        't_spike_dur': 0.5,
        'g_L':   25.0,
        'C_m':  500.0,
        'E_ex':   0.0,
        'E_in': -70.0,
        'E_L':  -70.0,
        'V_m':  -55.0,
        'ratio_NMDA_AMPA': 1.0,
        'tau_AMPA_rise': 0.5,
        'tau_AMPA_fall': 2.4,
        'tau_GABA_rise': 1.0,
        'tau_GABA_fall': 7.0,
        'tau_NMDA_rise': 5.5,
        'tau_NMDA_fall': 100.,
        }
    lat_ex_input_ports = [1]  # NMDA-AMPA input
    noise_firing_rate = 50000.
    noise_amplitude = 0.05275  # in objsim: 0.05294 to get 3 Hz background noise


class InhibitoryNeuron(NeuronSetup):

    model = 'iaf_cond_diffexp_ang'
    para_dict = {
        'V_th': -50.0,
        'V_reset': -55.0,
        't_ref': 1.0,
        't_spike_dur': 0.5,
        'g_L':   20.0,
        'C_m':  200.0,
        'E_ex':   0.0,
        'E_in': -70.0,
        'E_L':  -70.0,
        'V_m':  -55.0,
        'ratio_NMDA_AMPA': 1.0,
        'tau_AMPA_rise': 0.5,
        'tau_AMPA_fall': 2.4,
        'tau_GABA_rise': 1.0,
        'tau_GABA_fall': 7.0,
        'tau_NMDA_rise': 5.5,
        'tau_NMDA_fall': 100.,
        'const_GABA_input': 4.62,  # to reduce background noise to 3 Hz
    }
    lat_ex_input_ports = [1]  # NMDA-AMPA input
    noise_firing_rate = 50000.
    noise_amplitude = 0.0504967   # to get 100 Hz background noise