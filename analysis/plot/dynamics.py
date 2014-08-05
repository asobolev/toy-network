import numpy as np

from matplotlib.pyplot import figure
from matplotlib.collections import LineCollection


def multiple_time_series(events, times):
    """
    Creates a plot of multiple time series given.

    :param events:  2D (numpy) array with actual event values
    :param times:   1D (numpy) array with times
    """
    num_rows = len(events)

    fig = figure(figsize=(15, 10))
    ax = fig.add_subplot(111)

    # limits of the x axis
    ax.set_xlim(times[0], times[-1])

    # limits of the y axis
    dmin = events.min()
    dmax = events.max()
    dr = np.abs(dmax - dmin) * 1.15  # max height of a single row
    ax.set_ylim(0, num_rows * dr)

    segments = [zip(times, events[i]) for i in range(num_rows)]
    offsets = np.array(zip(np.zeros(num_rows), np.arange(num_rows) * dr - dmin))
    ax.add_collection(LineCollection(segments, offsets=offsets, transOffset=None))

    ax.set_yticks(np.arange(num_rows) * dr)
    ax.set_yticklabels(["N%s" % str(x) for x in range(num_rows)])

    ax.set_xlabel('time (ms)')
    ax.set_ylabel('events (N) with diff %f (ms)' % dr)

    return fig


def weight_matrix(ax, weights):
    """
    Paints given 2D weight matrix (with a colorbar) on the given axes.

    :param ax:      matplotlib axes where to plot
    :param weights: 2D matrix with float32 values
    """
    fig = figure(figsize=(15, 10))
    ax = fig.add_subplot(111)

    w_max = weights.max()
    w_min = weights.min()
    w_avg = (w_max + w_min) / 2
    delta = w_max - w_min

    weights_normalized = weights / w_max
    im = ax.imshow(weights_normalized, interpolation='nearest', origin='lower')

    bar = fig.colorbar(im)
    bar.set_ticks([round((w_min + (x * delta/10.0))/w_max, 2) for x in range(10)])
    bar.set_ticklabels([str(round(w_min + (x * delta/10.0), 2)) for x in range(10)])


def layer_co_dynamics(i_events, m_events, times):
    """
    Creates a plot of multiple time series given.

    :param events:  2D (numpy) array with actual event values
    :param times:   1D (numpy) array with times
    """
    fig = figure(figsize=(15, 10))
    ax_i = fig.add_subplot(211)
    ax_m = fig.add_subplot(212)

    for ax, events in zip([ax_i, ax_m], [i_events, m_events]):
        num_rows = len(events)

        # limits of the x axis
        ax.set_xlim(times[0], times[-1])

        # limits of the y axis
        dmin = events.min()
        dmax = events.max()
        dr = np.abs(dmax - dmin) * 1.15  # max height of a single row
        ax.set_ylim(0, num_rows * dr)

        segments = [zip(times, events[i]) for i in range(num_rows)]
        offsets = np.array(zip(np.zeros(num_rows), np.arange(num_rows) * dr - dmin))
        ax.add_collection(LineCollection(segments, offsets=offsets, transOffset=None))

        ax.set_yticks(np.arange(num_rows) * dr)
        ax.set_yticklabels(["N%s" % str(x) for x in range(num_rows)])

        ax.set_xlabel('time (ms)')
        ax.set_ylabel('events (N) with diff %f (ms)' % dr)

    return fig
