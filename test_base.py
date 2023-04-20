import json
from src import Anilist

query_client = Anilist.QueryClient()

print(query_client.media_list(username="xxxAnn", languages=["romaji", "english"]).entries)