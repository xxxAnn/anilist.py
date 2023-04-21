from Anilist.scheme import MediaScheme, Scheme
from Anilist.vars import Vars
from Anilist.client.client import Client
class MediaListQuery:
    
    def __init__(self, client: Client, username: str, per_page: int=10, starting_page: int = 1, languages=["english"], sizes=["extraLarge"], *, skip_init=False):
        self._username = username
        self._per_page = per_page
        self._starting_page = starting_page
        self._languages = languages
        self._client = client
        self._sizes = sizes
        self._media_entries = []

        self.DEFAULT_QUERY = [
            MediaScheme().id, 
            *[MediaScheme().title[lang] for lang in self._languages], 
            *[MediaScheme().coverImage[size] for size in self._sizes]
        ]
        self.DEFAULT_VARS = Vars(usr=self._username, page=self._starting_page, perPage=self._per_page)

        if not skip_init:
            self._base_query()

    @property
    def entries(self):
        return self._media_entries
    
    def query(self, *schs, default=True, vars=None):
    
        if default:
            schs = list(schs)
            schs.extend(self.DEFAULT_QUERY)
            if vars == None:
                vars = self.DEFAULT_VARS
            else:
                vars = Vars._merge(vars, self.DEFAULT_VARS)

        return self._query(*schs, vars=vars)
    
    def _query(self, *schs, vars):

        head_sch = Scheme().Page(page="$page", perPage="$perPage").mediaList(userName="$usr")

        q = self._client._create_query(vars, *schs, head_sch=head_sch)

        self._media_entries = self._client._page_request(q, vars, 'mediaList', f=lambda x: x.media)

    def _base_query(self):
        self.query()