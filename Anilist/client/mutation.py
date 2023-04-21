from Anilist.auth.auth import Auth
from Anilist.client.client import Client
from Anilist.mutation.media_list import MediaEntryMutable

import logging

class MutationClient(Client):

    def __init__(self, auth: Auth, level=logging.INFO, **kwargs):
        Client.__init__(self, auth, level, **kwargs)
    
    def _query_type(self):
        return "mutation"

    def media_entry(self, media_id):
        return MediaEntryMutable._from_media_id(self, media_id)
