# define wrappers for Anilist types

class AnilistType:
    def __new__(cls, v):
        if cls == AnilistType:
            if type(v) is str: 
                return AnilistString(None)
            if type(v) is int:
                return AnilistInt(None)
            if issubclass(v, AnilistType):
                return v
        else:
            return super().__new__(cls)

    def __str__(self):
        print(self.__class__)
        return self.__class__.ANILIST_TYPE_NAME
    
    def __repr__(self):
        return str(self)

class AnilistString(AnilistType):
    
    ANILIST_TYPE_NAME = "String"

class AnilistInt(AnilistType):

    ANILIST_TYPE_NAME = "Int"

