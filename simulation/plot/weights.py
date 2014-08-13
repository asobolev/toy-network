import numpy as np

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


def render_colorbar(image, axes, orientation, labels):
    """
    Draws a colorbar on a given axes for a given image.

    :param image:       image to build colorbar for
    :param axes:        axes where to render colorbar
    :param orientation: colorbar orientation, i.e. 'horizontal'
    :param labels:      float array with labels (11)
    """
    bar = plt.colorbar(image, cax=axes, orientation=orientation)

    bar.set_ticks(labels)
    bar.set_ticklabels([str(x) for x in labels])


def render_rectangular_matrix(axes, weights, xlabel, ylabel):
    """
    Draws a weight matrix on a given axes.
    Adds colorbar to a given colorbar axes (always horizontal).

    :param axes:        axes where to render plot
    :param weights:     numpy 2D array with weights
    """
    im = axes.imshow(weights, interpolation='nearest', origin='lower')

    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)

    return im


def weights_multiple(weights):
    """
    Creates a figure to plot several weight matrixes.

    :param weights: list of numpy 2D arrays with float values
    """

    fig = figure(figsize=(11, 7))
    fig.canvas.set_window_title('Weights input - map layers')

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
    Creates an image with neuron ids from a given layer.

    :param weights: list of numpy 2D arrays with float values
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
