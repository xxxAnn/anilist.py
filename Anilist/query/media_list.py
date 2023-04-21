from Anilist.scheme import MediaScheme, Scheme
from Anilist.vars.vars import Vars
class MediaListQuery:
    
    def __init__(self, client, username: str, per_page: int=10, starting_page: int = 1, languages=["english"], sizes=["extraLarge"]):
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
        # load default values
        self._base_query()

    @property
    def entries(self):
        return self._media_entries
    
    def query(self, *schs, default=True):
    
        if default:
            schs = list(schs)
            schs.extend(self.DEFAULT_QUERY)

        return self._query(*schs)
    
    def _query(self, *schs):

        head_sch = Scheme().Page(page="$page", perPage="$perPage").mediaList(userName="$usr")

        query = self._client._create_query(self.DEFAULT_VARS, *schs, head_sch=head_sch)

        pg = self._starting_page
        
        vals = self.DEFAULT_VARS._json

        temp = []

        while True:
            resp = self._client._request(query, vars=vals)
            data = ([v.media for v in resp.Page.mediaList])

            temp.extend(data)

            if data == []:
                break

            pg += 1
            vals["page"] = pg

        self._media_entries = temp

    def _base_query(self):
        self.query()