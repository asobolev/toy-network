
class NestObject(object):
    """
    An abstract class that represents any Nest object.
    """

    def __init__(self, id):
        self._nest_id = id

    @property
    def id(self):
        return self._nest_id


class Object2D(object):
    """
    An Interface for container objects that store elements as a 2D matrix.
    """

    def as_matrix(self):
        raise NotImplementedError()