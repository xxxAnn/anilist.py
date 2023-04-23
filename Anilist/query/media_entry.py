from Anilist.scheme import *
from Anilist.vars import Vars
from Anilist.client.client import Client
from Anilist.query.query import Query
class MediaEntryQuery(Query):
    """
    An interface for making Queries for media to the Anilist API

    
    .. warning::

        This usually should not be created manually, instead use :meth:`QueryClient.media_entry() <.client.QueryClient.media_entry>`

    """

    def __init__(self, client: Client, languages=["english"], sizes=["extraLarge"]):
        super().__init__(client, 'media', 'Media', [
            Scheme().id, 
            *[Scheme().title[lang] for lang in languages], 
            *[Scheme().coverImage[size] for size in sizes]
        ])