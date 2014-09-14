import numpy as np
from matplotlib.pyplot import figure


def multiple_line_plots(values, x_indexes, title=None):
    """
    Plots len(values) simple line plots on the same figure.
    Uses x_indices if given.

    :param values:      2D array, every row will be plotted on a different axes
    :param x_indices:   common x indexes to use
    :param title:       figure title
    """
    fig = figure(figsize=(15, 10))
    r_num = np.floor(np.sqrt(len(values)))
    c_num = np.ceil(len(values) / r_num)

    max_spikes = values.max()

    for nn, data in enumerate(values):
        ax = fig.add_subplot(r_num, c_num, nn + 1)
        ax.set_ylim(0, max_spikes)

        ax.set_xlabel('input neuron')
        ax.set_ylabel('number of spikes')

        ax.plot(x_indexes, data, 'o-')

    if title:
        fig.canvas.set_window_title(title)

    return fig
