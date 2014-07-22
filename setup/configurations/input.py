from __future__ import absolute_import
from reduced.setup.models import *


class ISGStraightGaussKernel(ISGStraightSetup):

    stimuli_duration = 20.
    i_s_i = 200.

    def __init__(self, movie_path):
        self.movie_path = movie_path