from Anilist.auth.auth import Auth
from Anilist.client.client import Client
from Anilist.mutation.media_list import MediaEntryMutable

class MutationClient(Client):

    def __init__(self, auth: Auth, level):
        Client.__init__(self, auth, level)

    def media_entry(self, media_id):
        return MediaEntryMutable._from_media_id(self, media_id)
