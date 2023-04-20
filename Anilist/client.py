import requests

from Anilist import Auth
from Anilist.mutation.media_list import MediaEntryMutable
from Anilist.obj import AnilistObject
from Anilist.query.media_list import MediaListQuery

class Client:

    URI = "https://graphql.anilist.co"
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, auth):
        self._auth = auth
        self._headers = None

    def _request(self, query, vars):
        req = requests.post(self.URI, json={
            "query": query,
            "variables": vars,
        }, headers = self.headers)

        obj = AnilistObject(req.json()["data"])
        if obj == None:
            print(req.json())
            return "ERR"
        return obj

    
    @property
    def headers(self):
        if self._headers == None:
            self._headers = self._gen_headers()
        
        return self._headers
        
    def _gen_headers(self):
        temp = self.DEFAULT_HEADERS

        if self._auth != None:
            temp["Authorization"] = f"Bearer {self._auth.token}"

        return temp
    
class QueryClient(Client):

    def __init__(self):
        Client.__init__(self, None)

    def media_list(self, **kwargs):
        return MediaListQuery(client=self, **kwargs)

    
class MutationClient(Client):

    def __init__(self, auth: Auth):
        Client.__init__(self, auth)

    def media_entry(self, media_id):
        return MediaEntryMutable._from_media_id(self, media_id)



