import nix
import numpy as np


class NixDumper(object):

    mode = {
        'readonly': nix.FileMode.ReadOnly,
        'overwrite': nix.FileMode.Overwrite
    }

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

    def get_neurons_for_layer(self, block_name, layer_name):
        block = self.get_block_by_name(block_name)

        layer = block.find_sources(lambda x: x.name == layer_name)[0]
        sources = layer.find_sources(lambda x: x.type == 'neuron')
        return sorted(sources, key=lambda x: int(x.name))

    def dump_stimulus(self, block_name, positions, extents, values):
        """
        Saves stimulus values in a block with a given name.

        :param block_name:  where to create a signal
        :param positions:   array of stimulus presentation times
        :param extents:     array of stimulus durations of each presentation
        :param values:      array of stimulus values for each presentation
        :return:            stimulus as MultiTag
        """
        def dump_array(name, unit, data):
            assert type(data[0]) == float

            iargs = [name, 'array', nix.DataType.Float, (len(data),)]
            simple_array = block.create_data_array(*iargs)
            simple_array.data[:] = data
            simple_array.unit = unit

            return simple_array

        block = self.get_block_by_name(block_name)

        positions = dump_array("stimulus positions", "ms", positions)
        extents = dump_array("stimulus extents", "ms", extents)
        stimulus = dump_array("stimulus", None, values)

        mt = block.create_multi_tag("stimulus", "stimulus", positions)
        mt.extents = extents
        mt.create_feature(stimulus, nix.LinkType.Indexed)

        return mt

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

        name = "%s_analogsignal" % str(source_name)
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

        name = "%s_spiketrain" % str(source_name)
        iargs = [name, 'spiketrain', nix.DataType.Float, (len(times),)]
        spiketrain = block.create_data_array(*iargs)

        spiketrain.data[:] = times
        spiketrain.unit = "ms"
        spiketrain.append_set_dimension()
        spiketrain.sources.append(neuron)

        return spiketrain

    def dump_weights(self, block_name, sources, targets, times, weights):
        """
        Saves synaptic weight dynamics as 3D matrix.

        :param block_name:  where to create weight matrix
        :param sources:     list of source neuron NEST IDs (int)
        :param targets:     list of target neuron NEST IDs (int)
        :param times:       time domain (floats)
        :param weights:     actual weight values (floats)
        :return:            created weight matrix as DataArray object
        """
        block = self.get_block_by_name(block_name)

        wargs = ['weights', 'synapses', nix.DataType.Float, weights.shape]
        matrix = block.create_data_array(*wargs)

        matrix.data[:] = weights
        matrix.append_range_dimension(sources)
        matrix.append_range_dimension(targets)
        matrix.append_range_dimension(times)
        matrix.dimensions[2].unit = 'ms'

        return matrix


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