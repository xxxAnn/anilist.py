from Anilist.scheme import *
from Anilist.vars import Vars
from Anilist.client.client import Client
from Anilist.query.query import Query
class MediaEntryQuery(Query):
    """
    An interface for making Queries for media to the Anilist API
    """

    def __init__(self, client: Client, languages=["english"], sizes=["extraLarge"]):
        super().__init__(client, 'media', 'Media', MediaScheme, mediaScheme, [
            Scheme().id, 
            *[Scheme().title[lang] for lang in languages], 
            *[Scheme().coverImage[size] for size in sizes]
        ])