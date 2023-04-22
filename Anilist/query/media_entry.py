from Anilist.scheme import *
from Anilist.vars import Vars
from Anilist.client.client import Client
from Anilist.query.query import Query
class MediaEntryQuery(Query):
    """
    An interface for making Queries for media to the Anilist API
    """
    def __init__(self, client: Client, languages=["english"], sizes=["extraLarge"]):
        super().__init__()
        self._languages = languages
        self._sizes = sizes
        self._client = client
        self._results = []

        self.DEFAULT_QUERY = [
            Scheme().id, 
            *[Scheme().title[lang] for lang in self._languages], 
            *[Scheme().coverImage[size] for size in self._sizes]
        ]


    def _query(self, *schs: Scheme, vars, head_sch, paginate=False, page=1, per_page=100):
        r = []

        if not paginate:

            q = self._client._create_query(vars, *schs, head_sch=head_sch)
            resp = self._client._request(q, vars._json)

            r.append(resp.Media)

        else:

            vars = Vars._merge(vars, Vars(page=page, perPage=per_page))
            q = self._client._create_query(vars, *schs, head_sch=Scheme._combine(Scheme().Page(page = '$page', perPage = '$perPage'), head_sch))

            r = self._client._page_request(q, vars, 'media')
        
        self._results = r

    def query(self, *schs: Scheme, vars, default=True, paginate=False, page=1, per_page=100):
        # this is for interacting in the most direct way with the Internal API 
        if default:
            schs = list(schs)
            schs.extend(self.DEFAULT_QUERY)

        return self._query(*schs, vars=vars,  head_sch=Scheme(), paginate=paginate, page=page, per_page=per_page)
    
    def search(self, *schs: Scheme, default=True, per_page: int=100, page: int=1, paginate=False, **kwargs):
        # the main way to interact with this object
        vars = Vars(**kwargs)

        if default:
            schs = list(schs)
            schs.extend(self.DEFAULT_QUERY)

        head_sch = mediaScheme(**vars._as_query()) if paginate else MediaScheme(**vars._as_query())
        return self._query(*schs, vars=vars, head_sch=head_sch, per_page=per_page, page=page, paginate=paginate)
