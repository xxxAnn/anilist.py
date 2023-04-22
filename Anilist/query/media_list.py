from Anilist.scheme import *
from Anilist.vars import Vars
from Anilist.client.client import Client
from Anilist.query.query import Query
class MediaListQuery(Query):
    """
    An interface for making Queries for media lists to the Anilist API
    """
    
    def __init__(self, client: Client, per_page: int=10, starting_page: int = 1, languages=["english"], sizes=["extraLarge"]):
        super().__init__()
        self._per_page = per_page
        self._starting_page = starting_page
        self._languages = languages
        self._client = client
        self._sizes = sizes
        self._media_entries = []

        self.DEFAULT_QUERY = [
            mediaScheme().id, 
            *[mediaScheme().title[lang] for lang in self._languages], 
            *[mediaScheme().coverImage[size] for size in self._sizes]
        ]
    
    def _query(self, *schs: Scheme, vars, head_sch, paginate=True, page=1, per_page=100):
        r = []

        if not paginate:

            q = self._client._create_query(vars, *schs, head_sch=head_sch)
            resp = self._client._request(q, vars._json)

            r.append(resp.Media)

        else:

            vars = Vars._merge(vars, Vars(page=page, perPage=per_page))
            q = self._client._create_query(vars, *schs, head_sch=Scheme._combine(Scheme().Page(page = '$page', perPage = '$perPage'), head_sch))

            r = self._client._page_request(q, vars, 'mediaList')
        
        self._results = r

    def query(self, *schs: Scheme, vars, head_sch, default=True, paginate=False, page=1, per_page=100):
        # this is for interacting in the most direct way with the Internal API 
        if default:
            schs = list(schs)
            schs.extend(self.DEFAULT_QUERY)

        return self._query(*schs, head_sch=head_sch, vars=vars, paginate=paginate, page=page, per_page=per_page)
    
    def search(self, *schs: Scheme, default=True, per_page: int=100, page: int=1, paginate=False, **kwargs):
        # the main way to interact with this object
        vars = Vars(**kwargs)

        if default:
            schs = list(schs)
            schs.extend(self.DEFAULT_QUERY)

        head_sch = MediaListScheme(**vars._as_query()) if not paginate else mediaListScheme(**vars._as_query())
        return self._query(*schs, head_sch=head_sch, vars=vars, paginate=paginate, per_page=per_page, page=page)
