# define wrappers for Anilist types

class AnilistType:
    def __new__(cls, v):
        if cls == AnilistType:
            if type(v) is str: 
                return AnilistString(None)
            if type(v) is int:
                return AnilistInt(None)
            if type(v) is float:
                return AnilistFloat(None)
            if isinstance(v, AnilistType):
                return v
        else:
            return super().__new__(cls)

    def __str__(self):
        return self.__class__.ANILIST_TYPE_NAME
    
    def __repr__(self):
        return str(self)
    
    def get_inner(self):
        return None

class AnilistString(AnilistType):
    
    ANILIST_TYPE_NAME = "String"

class AnilistInt(AnilistType):

    ANILIST_TYPE_NAME = "Int"

class AnilistFloat(AnilistType):

    ANILIST_TYPE_NAME = "Float"

class AnilistMediaType(AnilistType):
    
    ANILIST_TYPE_NAME = "MediaType"

    def __init__(self, s):
        self._inner = s

    def get_inner(self):
        return self._inner
    

