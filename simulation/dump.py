import nix
import numpy as np


class NixDumper(object):

    def __init__(self, filepath, mode=nix.FileMode.ReadOnly):
        self._path = filepath
        self._nf = nix.File.open(self._path, mode)

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, traceback):
        self._nf.close()
        if ex_type:
            return False

    def create_block(self, name, input_layer, map_layer):
        block = self._nf.create_block(name, 'simulation')

        layer_i = block.create_source('input_layer', 'layer')
        layer_m = block.create_source('map_layer', 'layer')

        new_neuron = lambda id: layer_i.create_source(str(id), 'neuron')
        map(new_neuron, input_layer.nodes)

        new_neuron = lambda id: layer_m.create_source(str(id), 'neuron')
        map(new_neuron, map_layer.nodes)

    def get_block_by_name(self, name):
        try:
            return filter(lambda x: x.name == str(name), self._nf.blocks)[0]
        except IndexError:
            raise NameError("Block with name %s does not exist" % name)

    def get_neuron_by_name(self, block_name, neuron_name):
        block = self.get_block_by_name(block_name)

        try:
            return block.find_sources(lambda x: x.name == str(neuron_name))[0]
        except IndexError:
            raise NameError("Source with name %s does not exist" % neuron_name)

    def dump_analogsignal(self, block_name, source_name, times, values):
        """
        Saves a signal with e.g. time series from neuron with ID as source_name
        in the block with a given name.

        :param block_name:  where to create a signal
        :param source_name: NEST ID of the neuron
        :param times:       time domain
        :param values:      actual values
        :return             created signal as DataArray object
        """
        block = self.get_block_by_name(block_name)
        neuron = self.get_neuron_by_name(block_name, source_name)

        name = "%s_v" % str(source_name)
        iargs = [name, 'analogsignal', nix.DataType.Float, (len(values),)]
        signal = block.create_data_array(*iargs)

        signal.data[:] = values
        signal.unit = 'mV'
        signal.append_range_dimension(times)
        signal.dimensions[0].unit = 'ms'
        signal.sources.append(neuron)

        return signal

    def dump_spiketrain(self, block_name, source_name, times):
        """
        Saves a spiketrain with spike events at times coming from neuron with ID
         source_name in the block with a given name.

        :param block_name:  where to create a spiketrain
        :param source_name: NEST ID of the neuron
        :param times:       times of spike events
        :return             created spiketrain as DataArray object
        """
        block = self.get_block_by_name(block_name)
        neuron = self.get_neuron_by_name(block_name, source_name)

        name = "%s_s" % str(source_name)
        iargs = [name, 'spiketrain', nix.DataType.Float, (len(times),)]
        spiketrain = block.create_data_array(*iargs)

        spiketrain.data[:] = times
        spiketrain.unit = "ms"
        spiketrain.append_set_dimension()
        spiketrain.sources.append(neuron)

        return spiketrain

    def dump_synapse(self, block_name, source, target, times, weights):
        """
        Saves synapse weight dynamics.

        :param block_name:  where to create a signal
        :param source:      NEST ID of the source neuron
        :param target:      NEST ID of the target neuron
        :param times:       time domain
        :param weights:     actual weight values
        :return             created synapse as DataArray object
        """
        block = self.get_block_by_name(block_name)
        source_neuron = self.get_neuron_by_name(block_name, source)
        target_neuron = self.get_neuron_by_name(block_name, target)

        name = "%s-%s" % (str(source), str(target))
        iargs = [name, 'synapse', nix.DataType.Float, (len(weights),)]
        synapse = block.create_data_array(*iargs)

        synapse.data[:] = weights
        synapse.append_range_dimension(times)
        synapse.dimensions[0].unit = 'ms'
        synapse.sources.append(source_neuron)
        synapse.sources.append(target_neuron)

        return synapse


def with_file_access(file_mode):
    """
    A decorator that open a NIX HDF5 file before method execution and closes
    the file after the method is finished.

    Example usage:

    @with_file_access(nix.FileMode.ReadWrite)
    def some_func(..):
        pass

    :param file_mode:   nix.FileMode to open the file
    """
    def actual_decorator(method):
        def call(self, *args, **kwargs):
            self._nf = nix.File.open(self._path, file_mode)
            result = method(self, *args, **kwargs)
            self._nf.close()
            return result
        return call
    return actual_decorator