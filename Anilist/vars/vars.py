from Anilist.anilist_types import AnilistType

class Vars:
    """
    Set of request variables that can be used in Schemes
    Each variable can be referenced by Schemes by prefixing their name with '$'

    Example::
        
        client = QueryClient()
        # $type and $search
        # reference the Vars' 'type' and 'search' kwargs
        schs = Scheme().Media(type="$type", search="$search").sub_schemes(
            Scheme().id,
            Scheme().title.english
        )
        vars = Vars(type=AnilistMediaType("ANIME"), search="One Piece")
        result = client._request(client._create_query(vars, *schs), vars)

        ## This is equivalent to using the following shortcut:
        media_search = QueryClient().media_entry()
        media_search.search(
            Scheme().id,
            Scheme().title.english,

            type=AnilistMediaType("ANIME"),
            search="One Piece"
        )
        result = media_search.results_take_one()
    """
    
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

    def update(self, k, v):
        if isinstance(v, AnilistType):
            self._dic[k] = v.get_inner()
        else:
            self._dic[k] = v

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
