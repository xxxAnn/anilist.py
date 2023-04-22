from Anilist.client.client import Client
from Anilist.mutation.mutable import Mutable
from Anilist.scheme import Scheme
from Anilist.vars import Vars


class MediaEntryMutable(Mutable):
    
    def __init__(self, id, client: Client):
        self._id = id
        self._client = client

    def set_score(self, score: float):

        self._mutate(Scheme().id, Scheme().score, head_sch=Scheme().SaveMediaListEntry, id=self._id, score=score)

        return "OK"
    
    def delete(self):
        
        self._mutate(Scheme().deleted, head_sch=Scheme().DeleteMediaListEntry, id=self._id)

        return "OK"

    @classmethod
    def _from_media_id(cls, client: Client, media_id):
        vars = Vars(mediaId=media_id)
        q = client._create_query(vars, Scheme().id, head_sch=Scheme().SaveMediaListEntry(mediaId='$mediaId'))

        resp = client._request(q, vars)

        return cls(resp.SaveMediaListEntry.id, client)
