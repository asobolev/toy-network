import numpy as np

from scipy.interpolate import pchip
from matplotlib.pyplot import figure
from matplotlib.collections import LineCollection
from render.raster import *


# ----------------
# Helper functions
# ----------------

def get_interpolated(x, y):
    # dense x and interpolator for the smooth curve for plotting
    xx = np.linspace(x[0], x[-1], len(x) * 10)
    interp = pchip(x, y)
    return xx, interp(xx)


# ------------------
# Plotting functions
# ------------------

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
    ax.set_ylabel('events (N) with diff %f (mV)' % dr)

    ax.grid()

    return fig


def layer_co_dynamics(i_events, m_events, times):
    """
    Creates a plot of multiple time series given.

    :param events:  2D (numpy) array with actual event values
    :param times:   1D (numpy) array with times
    """
    fig = figure(figsize=(15, 10))

    title = 'Input (top) and map (bottom) neurons voltage traces'
    fig.canvas.set_window_title(title)

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
        ax.set_ylabel('events (N) with diff %f (mV)' % dr)

    return fig


def raster_plot(times, senders):
    """
    Draws a raster plot of given events (times) with senders on a given axes.

    :param times:   array of times of events happened
    :param senders: array of IDs of event senders corresponding to given times
    :return         a raster plot figure
    """
    fig = figure(figsize=(15, 10))
    ax = fig.add_subplot(111)
    ax.set_ylim(senders.min() - 1, senders.max() + 1)

    render_raster(ax, times, senders)

    title = 'Spike events'
    fig.canvas.set_window_title(title)

    return fig


def single_line(x, y, title=None):
    """
    Plots a single line x, y.

    :param x:   x-values
    :param y:   y-values
    """
    fig = figure(figsize=(11, 7))

    ax = fig.add_subplot(111)

    ax.set_xlabel('time (ms)')
    ax.set_ylabel('total weight sum')
    ax.plot(*get_interpolated(x, y))
    ax.grid(True)

    if title:
        fig.canvas.set_window_title(title)

    return fig
