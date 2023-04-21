from Anilist import QueryClient, Scheme
from Anilist.anilist_types import AnilistMediaType

from Anilist.scheme import MediaScheme
from Anilist.vars import Vars

import logging
from unittest import TestCase

class BaseTest(TestCase):

    def test_scheme(self):
        _ = Scheme._construct(Scheme().A.B(k='$3'), Scheme().A.B.C, Scheme().A.B.C(k="$4").D)
    
    def test_query(self):
        q = QueryClient(max_pages=10)

        q.media_list(username="xxxAnn", per_page=100).entries[0]
        entry_query = q.media_entry()

        entry_query.query(*[
            MediaScheme(type='$mType').tags.id,
            MediaScheme().tags.name
        ], vars=Vars(mType=AnilistMediaType("ANIME")), paginate=True)

        print(entry_query.results_take_all())