from Anilist.anilist_types import AnilistType

class Vars:
    
    def __init__(self, **kwargs):
        dic = dict(kwargs)
        l = []
        for k, v in dic.items(): 
            l.append(f"${k}: {AnilistType(v).__class__.ANILIST_TYPE_NAME}")

        self._dic = dic
        self._vars = l

    @property
    def _names(self):
        return ', '.join(self._vars)
    
    @property
    def _json(self):
        return self._dic