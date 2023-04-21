from Anilist.scheme import MediaScheme, Scheme
from Anilist.vars import Vars
from Anilist.client.client import Client

class MediaEntryQuery:

    def __init__(self, client: Client, languages=["english"], sizes=["extraLarge"]):

        self._languages = languages
        self._sizes = sizes
        self._client = client
        self._results = []

        self.DEFAULT_QUERY = [
            MediaScheme().id, 
            *[MediaScheme().title[lang] for lang in self._languages], 
            *[MediaScheme().coverImage[size] for size in self._sizes]
        ]


    def _query(self, *schs: Scheme, vars, paginate=False, page=1, per_page=100):
        r = []

        if not paginate:

            q = self._client._create_query(vars, *[sch._replace_head("media", "Media") for sch in schs])
            resp = self._client._request(q, vars._json)

            r.append(resp.Media)

        else:

            head_sch = Scheme().Page(page = '$page', perPage = '$perPage')
            vars = Vars._merge(vars, Vars(page=page, perPage=per_page))
            q = self._client._create_query(vars, *[sch._replace_head("Media", "media") for sch in schs], head_sch=head_sch)

            r = self._client._page_request(q, vars, 'media')
        
        self._results = r

    def query(self, *schs: Scheme, vars, default=True, paginate=False, page=1, per_page=100):

        if default:
            schs = list(schs)
            schs.extend(self.DEFAULT_QUERY)

        return self._query(*schs, vars=vars, paginate=paginate, page=page, per_page=per_page)

    def results_take_all(self):
        r = self._results
        self._results = []
        return r
    
    def results_take_front(self):
        r = self._results[0]
        self._results = self._results[1:]
        return r
    
    def results_take_back(self):
        r = self._results[-1]
        self._results = self._results[:-1]
        return r


