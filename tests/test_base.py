from Anilist import QueryClient, Scheme
from Anilist.anilist_types import AnilistMediaType

from Anilist.scheme import mediaScheme
from Anilist.vars import Vars

import logging
from unittest import TestCase

class BaseTest(TestCase):

    def test_scheme(self):
        _ = Scheme._construct(Scheme().A.B(k='$3'), Scheme().A.B.C, Scheme().A.B.C(k="$4").D)
    
    def test_query(self):
        q = QueryClient(max_pages=10)

        list_query = q.media_list(per_page=100)
        list_query.search(
            mediaScheme().coverImage.medium,

            paginate=True, 
            userName="xxxAnn"
        )

        entry_query = q.media_entry()
        entry_query.search(
            Scheme().tags.id,
            Scheme().tags.name,
            
            type = AnilistMediaType('ANIME')
        )
        
        print(list_query.results_take_front())
        print('\n')
        print(entry_query.results_take_front())