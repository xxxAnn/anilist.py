    
from Anilist.client import Client
from Anilist.query import MediaEntryQuery
from Anilist.query import MediaListQuery

import logging

from Anilist.vars.vars import Vars

class QueryClient(Client):
    """
    A hub that creates various interfaces that interact with the Anilist API

    :param level: The logging level for this client
    :type level: :class:`~int`   
    """

    def __init__(self, level=logging.INFO, **kwargs):
        """Constructor method
        """
        Client.__init__(self, None, level, **kwargs)

    def _query_type(self):
        return "query"

    def media_list(self, *, languages=["english"], sizes=["extraLarge"]):
        """Creates a :class:`~.query.MediaListQuery` object
        """
        return MediaListQuery(client=self, languages=languages, sizes=sizes)
    
    def media_entry(self, *, languages=["english"], sizes=["extraLarge"]):
        """Creates a :class:`~.query.MediaEntryQuery` object
        """
        return MediaEntryQuery(client=self, languages=languages, sizes=sizes)
