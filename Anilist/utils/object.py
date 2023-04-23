class AnilistObject:
    """An object representing data sent by the Anilist API
    
    .. warning:: 
    
        This should never be created manually

    .. note::
        
        The attributes for any specific :class:`~AnilistObject` are the same as for the :class:`~.scheme.Scheme` provided in the request

    Example:

    .. code-block:: python

        ###! In a raw Client request
        client = Anilist.QueryClient()
        query = \"\"\"
            Media (type: $type, search: $search) {
                id
                title {
                    english
                }
            }
        \"\"\"
        result = client._request(
            query,
            vars=Vars(type=AnilistMediaType("ANIME"), search="One Piece")
        )
        # result is an AnilistObject with the following attributes
        id = result.Media.id
        english_title = result.Media.title.english

        ###! In a basic Client request
        client = Anilist.QueryClient()
        schs = Scheme().Media(type="$type", search="$search").sub_schemes(
            Scheme().id,
            Scheme().title.english
        )
        vars = Vars(type=AnilistMediaType("ANIME"), search="One Piece")
        result = client._request(client._create_query(vars, *schs), vars)

        # result is an AnilistObject with the following attributes
        id = result.Media.id
        english_title = result.Media.title.english

        

        ###! Using the Query API
        media_search = Anilist.QueryClient().media_entry()
        media_search.search(
            Scheme().id,
            Scheme().title.english,

            type=AnilistMediaType("ANIME"),
            search="One Piece"
        )
        result = media_search.results_take_one()

        # The Query API automatically returns 
        # only the inner part of the request
        # so you do not need to do 'result.Media'
        # result is an AnilistObject with the following attributes
        id = result.id
        english_title = result.title.english
        # This one is added because the MediaEntryQuery API 
        # has coverImage.extraLarge as a default field to query
        extra_large_cover = result.coverImage.extraLarge
        
    """
    
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
    
    def __getitem__(self, k):
        return self.__dict[k]
    
    def __str__(self):
        return str(self.__dict)
    
    def __repr__(self):
        return str(self)