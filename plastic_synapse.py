import nest
import numpy as np
import matplotlib.pyplot as plt

from plot import *


def execute():
    nest.ResetKernel()

    # single input neuron
    input_neuron = nest.Create("iaf_psc_alpha")

    # single output neuron
    output_neuron = nest.Create("iaf_psc_alpha")

    # plastic connection
    nest.CopyModel('stdp_synapse_hom', 'plastic', {'alpha': 0.1, 'Wmax': 1000.})

    kwargs = {
        'params': {'weight': 250.},
        'model': 'plastic',  #'stdp_pl_norm_synapse_hom'
    }
    nest.Connect(input_neuron, output_neuron, **kwargs)
    connection = nest.GetConnections(input_neuron, output_neuron)

    # voltmeters setup
    monitors = []
    rec_params = {'record_from': ['V_m'], 'withtime': True}
    for node in [input_neuron, output_neuron]:
        voltmeter = nest.Create('multimeter', params=rec_params)
        nest.Connect(voltmeter, node)
        monitors.append(voltmeter[0])

    # simulation
    scales = []
    for t in range(10):  # 10 seconds in total
        state = nest.GetStatus(connection)[0]
        scales.append(state)

        dc = nest.Create("dc_generator")
        nest.SetStatus(dc, [{
            "amplitude": 700.0,
            "start": t*1000.0 + 200.0,
            "stop": t*1000.0 + 800.0
        }])

        nest.ConvergentConnect(dc, input_neuron)

        nest.Simulate(1000.0)

    # analysis
    print scales

    output = []
    for node_id in monitors:
        output.append(nest.GetStatus([node_id], 'events')[0])

    events = np.array([event['V_m'] for event in output])
    fig = multiple_time_series(events, output[0]['times'])

    plt.show()


if __name__ == '__main__':
    execute()