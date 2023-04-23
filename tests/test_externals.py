from Anilist import QueryClient, Scheme, MutationClient, MediaScheme
from Anilist.anilist_types import AnilistMediaType
from Anilist import Auth

from Anilist.scheme import mediaScheme
from Anilist.vars import Vars

import logging
from unittest import TestCase

class ExternalsTest(TestCase):

    def test_auth(self):
        auth = Auth.from_config_file("config.json")
        a = MutationClient(auth, max_pages=10)

        a.media_entry(103572).set_score(35.0)

    
    def test_query(self):
        q = QueryClient(max_pages=10)

        list_query = q.media_list()
        list_query.search(
            # Fields to Query
            mediaScheme().coverImage.medium,
            
            # Search settings
            per_page = 100,
            paginate = True, 

            # Query parameters
            userName="xxxAnn"

        )

        entry_query = q.media_entry()
        entry_query.search(
            # Fields to Query
            Scheme().tags.id,
            Scheme().tags.name,

            # Search settings

            #Query parameters
            type = AnilistMediaType('ANIME'),
            search = "One Piece"

        )
        
        print(list_query.results_take_front())
        print('\n')
        print(entry_query.results_take_front())