import numpy as np
import matplotlib.pyplot as plt


def render_colorbar(axes, image, orientation, vmin, vmax):
    """
    Draws a colorbar on a given axes for a given image.

    :param axes:        axes where to render colorbar
    :param image:       image to build colorbar for
    :param orientation: colorbar orientation, i.e. 'horizontal'
    :param vmin:        min value of the labels (11)
    :param vmax:        max value of the labels (11)
    """
    bar = plt.colorbar(image, cax=axes, orientation=orientation)

    delta = vmax - vmin
    labels = [round((vmin + (x * delta/10.0)), 2) for x in range(11)]

    bar.set_ticks(labels)
    bar.set_ticklabels([str(x) for x in labels])

    return bar


def render_rectangular_matrix(axes, weights, xlabel, ylabel):
    """
    Draws a weight matrix on a given axes.
    Adds colorbar to a given colorbar axes (always horizontal).

    :param axes:        axes where to render plot
    :param weights:     numpy 2D array with weights
    """
    kwargs = {
        'interpolation': 'nearest',
        'origin': 'lower',
        'aspect': 'auto'
    }
    im = axes.imshow(weights, **kwargs)

    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)
    axes.grid()

    return im