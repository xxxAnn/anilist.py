import requests, logging

from Anilist import Auth, consts
from Anilist.mutation.media_list import MediaEntryMutable
from Anilist.object import AnilistObject
from Anilist.query.media_list import MediaListQuery
from Anilist.logging import AnilistLogger

class Client:

    URI = consts.API_URI
    DEFAULT_HEADERS = consts.DEFAULT_HEADERS

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



