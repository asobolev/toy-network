
def render_raster(ax, times, senders):
    """
    Draws a raster plot of given events (times) with senders on a given axes.

    :param ax:      axes object where to draw
    :param times:   array of times of events happened
    :param senders: array of IDs of event senders corresponding to given times
    """
    ax.plot(times, senders, '.')
    ax.set_xlabel('time (ms)')
    ax.set_ylabel('sender ID')
    ax.grid()