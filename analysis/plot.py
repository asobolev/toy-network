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


def weight_matrix(weights):
    """
    Creates an matrix image with colorbar for a given 2D weight matrix.

    :param weights: 2D matrix with float32 values between 0.0 and 1.0
    """
    fig = figure(figsize=(15, 10))
    ax = fig.add_subplot(111)

    im = ax.imshow(weights, interpolation='nearest', origin='lower')
    fig.colorbar(im)

    return fig