from Anilist.scheme import Scheme
from Anilist.vars import Vars


class Mutable:

    def __init__(self, client):
        self._client = client
    
    def _mutate(self, *schs: Scheme, head_sch: Scheme, **kwargs):
        
        v = Vars(**kwargs)
        q = self._client._create_query(v, *schs, head_sch=head_sch(**v._as_query()))

        return self._client._request(q, v)