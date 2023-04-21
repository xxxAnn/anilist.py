class AnilistObject:
    
    def __init__(self, json_object):
        self.__dict = {}
        for k, v in json_object.items():
            if type(v) is dict:
                self.__dict[k] = AnilistObject(v)
            elif type(v) is list:
                self.__dict[k] = [AnilistObject(el) if type(el) is dict else el for el in v]
            else:
                self.__dict[k] = v

    def __getattr__(self, k):
        return self.__dict[k]
    
    def __str__(self):
        return str(self.__dict)
    
    def __repr__(self):
        return str(self)