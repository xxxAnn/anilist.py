from .scheme import Scheme

class MediaScheme(Scheme):
    def __init__(self, **kwargs):
        super().__init__()
        self._layers.append("Media")
        self(**kwargs)

class mediaScheme(Scheme):
    def __init__(self, **kwargs):
        super().__init__()
        self._layers.append("media")
        self(**kwargs)

class mediaListScheme(Scheme):
    def __init__(self, **kwargs):
        super().__init__()
        self._layers.append("mediaList")
        self(**kwargs)

class MediaListScheme(Scheme):
    def __init__(self, **kwargs):
        super().__init__()
        self._layers.append("MediaList")
        self(**kwargs)