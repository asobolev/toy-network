import nest
from nest import voltage_trace



def execute():
    nest.ResetKernel()

    # single input neuron
    input_neuron = nest.Create("iaf_psc_alpha")

    # single output neuron
    output_neuron = nest.Create("iaf_psc_alpha")

    # plastic connection
    nest.Connect(input_neuron, output_neuron, model='stdp_pl_norm_synapse_hom')

    # voltmeter
    rec_params = {'record_from': ['V_m'], 'withtime': True}
    voltmeter = nest.Create('multimeter', params=rec_params)
    nest.Connect(voltmeter, input_neuron)

    for t in range(10):  # 10 seconds in total
        dc = nest.Create("dc_generator")
        nest.SetStatus(dc, [{
            "amplitude": 100.0,
            "start": t*1000.0 + 200.0,
            "stop": t*1000.0 + 500.0
        }])

        nest.ConvergentConnect(dc, input_neuron)

        nest.Simulate(1000.0)

    voltage_trace.from_device(voltmeter)
    voltage_trace.show()


if __name__ == '__main__':
    execute()