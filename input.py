import nest


INPUT_MOVIE = 'data/gauss20x20.idlmov'


class ImageSequenceGeneratorSetup(object):

    def __init__(self, movie_path, stimuli_duration, stimuli_per_object, nx, ny,
                 pre_ISI=2.5, post_ISI=2.5, type='xysequence',
                 stim_direction='x_continuous'):
        self.movie_path = movie_path
        self.stimuli_duration = stimuli_duration
        self.stimuli_per_object = stimuli_per_object
        self.nx = nx
        self.ny = ny
        self.pre_ISI = pre_ISI
        self.post_ISI = post_ISI
        self.type = type
        self.stim_direction = stim_direction

    @property
    def _player_parameters(self):
        return {
            'stimulus_interval': self.stimuli_duration,
            'inter_stimulus_interval': self.pre_ISI,
            'inter_stimulus_interval2': self.post_ISI,
            'stimuli_per_object': self.stimuli_per_object,
            'nx': self.nx,
            'ny': self.ny,
            'stim_direction': self.stim_direction
        }

    @property
    def _player(self):
        return {
            'type': self.type,
            'parameter': self._player_parameters
        }

    @property
    def as_dict(self):
        return {
            'filename': self.movie_path,
            'player': self._player
        }


def image_sequence_generator_showcase():

    pre_ISI = 2.0
    post_ISI = 2.5
    stimuli_duration = 20.0
    stimuli_per_object = 5
    nx = 20
    ny = 20
    single_stim_time = stimuli_duration + pre_ISI

    ISG_config = ImageSequenceGeneratorSetup(
        INPUT_MOVIE, stimuli_duration, stimuli_per_object, nx, ny
    )

    nest.ResetKernel()
    img_seq = nest.Create('image_sequence_generator', 1, ISG_config.as_dict)

    nest.Simulate(0.5 * single_stim_time)

    import ipdb
    ipdb.set_trace()

    for i in range(stimuli_per_object):
        frame_num = nest.GetStatus(img_seq, 'current_frame_num')[0]
        nest.Simulate(single_stim_time)


if __name__=='__main__':
    image_sequence_generator_showcase()
