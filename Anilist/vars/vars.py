from Anilist.anilist_types import AnilistType

class Vars:
    
    def __init__(self, **kwargs):
        dic = dict(kwargs)
        l = []
        for k, v in dic.items(): 
            if isinstance(v, AnilistType):
                dic[k] = v.get_inner()
                l.append(f"${k}: {v.__class__.ANILIST_TYPE_NAME}")
            else:
                l.append(f"${k}: {AnilistType(v).__class__.ANILIST_TYPE_NAME}")


        self._dic = dic
        self._vars = l

    def _as_query(self):
        temp = {}

        for k, v in self._dic.items():
            temp[k] = f"${k}"

        return temp

    @property
    def _names(self):
        return ', '.join(self._vars)
    
    @property
    def _json(self):
        return self._dic
    
    @classmethod 
    def _merge(cls, vara, varb):
        n = Vars()

        n._vars = vara._vars + varb._vars
        n._dic = vara._dic | varb._dic

        return n
