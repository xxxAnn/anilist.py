import requests, logging

from Anilist import Auth
from Anilist.mutation.media_list import MediaEntryMutable
from Anilist.obj import AnilistObject
from Anilist.query.media_list import MediaListQuery
from Anilist.logging import AnilistLogger

class Client:

    URI = "https://graphql.anilist.co"
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, auth, level):
        self._auth = auth
        self._headers = None
        _ = AnilistLogger(level)

    def _request(self, query, vars):
        log = AnilistLogger()
        log.info(f"Sending request to URI {self.URI} with headers {self.headers}")
        log.debug(f"The query is {query}\n The variables are {vars}")
        req = requests.post(self.URI, json={
            "query": query,
            "variables": vars,
        }, headers = self.headers)

        log.info(f"Received response to request with status code {req.status_code}")
        obj = AnilistObject(req.json()["data"])
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

    def __init__(self, level):
        Client.__init__(self, None, level)

    def media_list(self, *, username, per_page: int=10, starting_page: int=1, languages=["english"], sizes=["extraLarge"]):
        return MediaListQuery(
            client=self,
            username=username, 
            per_page=per_page, 
            starting_page=starting_page, 
            languages=languages, 
            sizes=sizes
        )

    
class MutationClient(Client):

    def __init__(self, auth: Auth, level):
        Client.__init__(self, auth, level)

    def media_entry(self, media_id):
        return MediaEntryMutable._from_media_id(self, media_id)



