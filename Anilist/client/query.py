    
from Anilist.client import Client
from Anilist.query.media_list import MediaListQuery

import logging

class QueryClient(Client):

    def __init__(self, level=logging.INFO):
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

    
