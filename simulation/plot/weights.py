import numpy as np
from matplotlib.pyplot import figure
from render.matrix import *


def weights_multiple(weights):
    """
    Creates a figure to plot several weight matrixes.

    :param weights: list of numpy 2D arrays with float values
    """

    fig = figure(figsize=(11, 7))
    fig.canvas.set_window_title('Weights input - map layers')

    # potentially using GridSpec for alignments
    #gs = gridspec.GridSpec(5, 1)
    #ax_r = fig.add_subplot(gs[:2, :])
    #ax_w = fig.add_subplot(gs[2:4, :])

    to_plot = np.array(weights)
    total = len(to_plot)
    g_min = to_plot.min()  # needed for colorbar
    g_max = to_plot.max()
    delta = g_max - g_min

    for i, matrix in enumerate(to_plot):
        key = 100 + total * 10 + (i+1)  # always horizontal
        ax = fig.add_subplot(key)

        weights_normalized = matrix
        im = ax.imshow(weights_normalized.T, vmin=g_min, vmax=g_max, interpolation='nearest', origin='lower')

        ax.set_xlabel('input neurons')
        ax.set_ylabel('map neurons')

    try:
        axc = fig.add_axes([0.1, 0.1, 0.8, 0.05])  # setup colorbar axes.
        bar = plt.colorbar(im, cax=axc, orientation='horizontal')

        labels = [round((g_min + (x * delta/10.0)), 2) for x in range(11)]
        bar.set_ticks(labels)
        bar.set_ticklabels([str(x) for x in labels])

    except NameError:
        pass

    return fig


def neuron_ids_in_layer(layer):
    """
    Creates an image with neuron ids as colors from a given layer.

    :param layer:   a Layer object
    """
    ids = [map(lambda x: float(getattr(x, 'id')), column) for column in layer.as_matrix]
    matrix = np.array(ids)

    fig = figure(figsize=(15, 10))
    ax = fig.add_subplot(111)

    w_max = matrix.max()
    w_min = matrix.min()
    delta = w_max - w_min

    weights_normalized = matrix / w_max
    im = ax.imshow(weights_normalized, interpolation='nearest', origin='lower')

    bar = fig.colorbar(im)
    bar.set_ticks([round((w_min + (x * delta/10.0))/w_max, 2) for x in range(10)])
    bar.set_ticklabels([str(round(w_min + (x * delta/10.0), 2)) for x in range(10)])

    return fig


def single_weight_evolution(weights, neuron_id):
    """
    Creates a weight evolution figure for a particular map neuron.

    :param weights: numpy 2D array with float values
    """
    fig = figure(figsize=(15, 10))

    ax_w = fig.add_axes([0.12, 0.2, 0.78, 0.75])
    ax_w.grid()
    xlabel = 'time steps'
    ylabel = 'input neurons'
    image = render_rectangular_matrix(ax_w, weights, xlabel, ylabel)

    ax_c = fig.add_axes([0.12, 0.1, 0.78, 0.03])  # axes for colorbar
    cbar = render_colorbar(ax_c, image, 'horizontal', weights.min(), weights.max())

    title = 'Weight evolution for neuron %s' % str(neuron_id)
    fig.canvas.set_window_title(title)

    return fig
