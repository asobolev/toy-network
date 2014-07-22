import nest
import nest.voltage_trace

import reduced.setup.configurations as conf

nest.ResetKernel()


input_neuron = nest.Create("iaf_neuron")
nest.SetStatus(neuron,[{"V_peak": 0.0, "a": 4.0, "b":80.5}])

output_neuron = nest.Create("iaf_neuron")
nest.SetStatus(neuron,[{"V_peak": 0.0, "a": 4.0, "b":80.5}])

nest.Connect(input_neuron, output_neuron, model='stdp_pl_norm_synapse_hom')


for t in range(10):
    dc=nest.Create("dc_generator",2)

    nest.SetStatus(dc,[{"amplitude":500.0, 
                        "start":0.0, 
                        "stop":200.0},
                       {"amplitude":800.0,
                        "start":500.0,
                        "stop":1000.0}])

    nest.ConvergentConnect(dc,neuron)

    voltmeter= nest.Create("voltmeter")
    nest.SetStatus(voltmeter,[{"to_file": True, "withtime": True}])
    nest.Connect(voltmeter,neuron)

    nest.Simulate(1000.0)
