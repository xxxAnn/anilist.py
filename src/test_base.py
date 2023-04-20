import json
import Anilist

s = Anilist.Scheme().Test.Test
s1 = Anilist.Scheme().Test.Base
s3 = Anilist.Scheme().Test.Base.Hi

print(Anilist.construct_query([s, s1, s3]))