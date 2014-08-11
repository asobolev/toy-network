import nest
from base import NestObject


class MonitorPool(object):

    def __init__(self, monitor_cls, neurons):
        self._monitors = [monitor_cls(node_id) for node_id in neurons]

    def __len__(self):
        return len(self._monitors)

    def __getitem__(self, key):
        return self._monitors[key]

    def __iter__(self):
        for i in range(0, len(self)):
            yield self.__getitem__(i)

    def __delitem__(self, key):
        raise NotImplementedError()

    def __str__(self):
        return str((list(self)))

    def __repr__(self):
        return str(self)


class VoltageMonitor(NestObject):

    def __init__(self, nest_node_id):
        rec_params = {'record_from': ['V_m'], 'withtime': True}

        self._nest_id = nest.Create('multimeter', params=rec_params)[0]
        nest.Connect([self._nest_id], [nest_node_id])

    @property
    def _get_data(self):
        return nest.GetStatus([self.id], 'events')[0]

    @property
    def V_m(self):
        return self._get_data['V_m']

    @property
    def senders(self):
        return self._get_data['senders']

    @property    
    def times(self):
        return self._get_data['times']


class SpikeDetector(NestObject):

    def __init__(self, nest_node_ids):

        self._nest_id = nest.Create('spike_detector')[0]
        nest.ConvergentConnect(nest_node_ids, [self._nest_id])

    @property
    def _get_data(self):
        return nest.GetStatus([self.id], 'events')[0]

    @property
    def senders(self):
        return self._get_data['senders']

    @property
    def times(self):
        return self._get_data['times']