import h5py
import numpy as np


class Dumper(object):
    """
    A simple class that saves important simulation results in an HDF5 file.

    TODO write a file open/close decorator
    """
    def __init__(self, path, mode='r'):
        def create_if_absent(group_name):
            if not group_name in f.keys():
                f.create_group(group_name)

        self._path = path
        self.f = None

        if mode == 'w':
            root_groups = ['synapses', 'spikes_input', 'spikes_map', 'voltage']
            with h5py.File(self._path, mode) as f:
                map(create_if_absent, root_groups)

    def _write_dynamic_data(self, group, times, values):
        def delete_if_exist(name):
            if name in group.keys():
                del group[name]

        group.create_dataset('times_temp', data=times)
        group.create_dataset('values_temp', data=values)

        map(delete_if_exist, ['times', 'values'])

        group['times'] = group['times_temp']
        group['values'] = group['values_temp']

        map(delete_if_exist, ['times_temp', 'values_temp'])

    def dump_input_spikes(self, times, senders):
        with h5py.File(self._path, 'r+') as f:
            group = f['spikes_input']
            self._write_dynamic_data(group, times, senders)

    def dump_map_spikes(self, times, senders):
        with h5py.File(self._path, 'r+') as f:
            group = f['spikes_map']
            self._write_dynamic_data(group, times, senders)

    def dump_synapse_snapshots(self, times, synapse_snapshots):
        with h5py.File(self._path, 'r+') as f:
            synapse_sample = synapse_snapshots[0]
            synapse_ids = [(x['source'], x['target']) for x in synapse_sample]

            weights = np.array([[x['weight'] for x in synapses] for synapses in synapse_snapshots])

            all_synapses = f['synapses']
            all_synapses.create_dataset('times', data=np.array(times))

            for i, id_pair in enumerate(synapse_ids):
                source, target = id_pair  # source, target are NEST ids

                name = "%s-%s" % (str(source), str(target))
                data = [x[i] for x in weights]
                syn = all_synapses.create_dataset(name, data=data)

                syn.attrs.create('source', source)
                syn.attrs.create('target', target)

    def dump_voltage_trace(self, neuron_id, times, values):
        with h5py.File(self._path, 'r+') as f:
            parent = f['voltage']
            if not str(neuron_id) in parent.keys():
                parent.create_group(str(neuron_id))

            self._write_dynamic_data(parent[str(neuron_id)], times, values)

