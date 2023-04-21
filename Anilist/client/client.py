import requests, logging
from Anilist.scheme.scheme import Scheme

from Anilist.utils import AnilistObject, AnilistLogger, consts
from Anilist.errors import RequestError
class Client:

    URI = consts.API_URI
    DEFAULT_HEADERS = consts.DEFAULT_HEADERS

    def __init__(self, auth, level, max_pages=100):
        self._auth = auth
        self._headers = None
        self._max = max_pages
        _ = AnilistLogger(level)

    def _page_request(self, query, vars, k, f=lambda x: x):        
        vals = vars._json
        pg = vals["page"]

        temp = []

        while pg <= self._max:
            resp = self._request(query, vars=vals)
            data = ([f(v) for v in resp.Page[k]])

            temp.extend(data)

            if data == []:
                break

            pg += 1
            vals["page"] = pg

        return temp

    def _request(self, query, vars):

        log = AnilistLogger()
        log.info(f"Sending request to URI {self.URI} with headers {self.headers}")
        log.debug(f"The query is {query}\n The variables are {vars}")
        
        req = requests.post(self.URI, json={
            "query": query,
            "variables": vars,
        }, headers = self.headers)

        resp = req.json()

        log.info(f"Received response to request with status code {req.status_code}")

        if "errors" in resp and resp["errors"] != []:
            raise RequestError.from_json(resp["errors"][0])
        
        obj = AnilistObject(resp["data"])
        return obj
        
    def _create_query(self, vars, *schs, head_sch=None):
        schs = list(schs) if head_sch is None else [Scheme._combine(head_sch, sch) for sch in schs]
        if vars._names == "":
            return """
            {} {{
                {}
            }}
            """.format(self._query_type(), Scheme._construct(*schs))
        return """
            {} ({}) {{
                {}
            }}
        """.format(self._query_type(), vars._names, Scheme._construct(*schs))

        return query
    
    def _query_type(self):
        return "null"
    
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



