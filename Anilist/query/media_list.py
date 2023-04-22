from Anilist.scheme import *
from Anilist.vars import Vars
from Anilist.client.client import Client
from Anilist.query.query import Query
class MediaListQuery(Query):
    """
    An interface for making Queries for media lists to the Anilist API
    """
    
    def __init__(self, client: Client, languages=["english"], sizes=["extraLarge"]):
        super().__init__(client, 'mediaList', 'MediaList', MediaListScheme, mediaListScheme, [
            mediaScheme().id, 
            *[mediaScheme().title[lang] for lang in languages], 
            *[mediaScheme().coverImage[size] for size in sizes]
        ])
    
    
