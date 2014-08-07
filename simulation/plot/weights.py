import numpy as np

from matplotlib.pyplot import figure


def weights_multiple(weights):
    """
    Creates a figure to plot several weight matrixes.

    :param weights: list of numpy 2D arrays with float values
    """

    fig = figure(figsize=(15, 10))
    fig.canvas.set_window_title('Weights input - map layers')

    total = len(weights)
    for i, matrix in enumerate(weights):
        key = 100 + total * 10 + (i+1)  # always horizontal
        ax = fig.add_subplot(key)

        w_max = matrix.max()
        w_min = matrix.min()
        delta = w_max - w_min

        weights_normalized = matrix / w_max
        im = ax.imshow(weights_normalized, interpolation='nearest', origin='lower')

        ax.set_xlabel('map neurons')
        ax.set_ylabel('input neurons')

        bar = fig.colorbar(im)
        bar.set_ticks([round((w_min + (x * delta/10.0))/w_max, 2) for x in range(10)])
        bar.set_ticklabels([str(round(w_min + (x * delta/10.0), 2)) for x in range(10)])

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