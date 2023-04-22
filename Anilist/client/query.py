    
from Anilist.client import Client
from Anilist.query import MediaEntryQuery
from Anilist.query import MediaListQuery

import logging

from Anilist.vars.vars import Vars

class QueryClient(Client):

    def __init__(self, level=logging.INFO, **kwargs):
        """
        Parameters
        ----------
        level : int
            The logging level for this client
        """
        Client.__init__(self, None, level, **kwargs)

    def _query_type(self):
        return "query"

    def media_list(self, *, per_page: int=10, starting_page: int=1, languages=["english"], sizes=["extraLarge"]):
        return MediaListQuery(
            client=self,
            per_page=per_page, 
            starting_page=starting_page, 
            languages=languages, 
            sizes=sizes
        )
    
    def media_entry(self, *, languages=["english"], sizes=["extraLarge"]):
        return MediaEntryQuery(client=self, languages=languages, sizes=sizes)
