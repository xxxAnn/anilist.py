from .scheme import Scheme


class MediaScheme(Scheme):
    def __init__(self, **kwargs):
        super().__init__()
        self._layers.append("media")
        self(**kwargs)
