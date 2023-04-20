import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../src'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))


from Anilist import QueryClient
import logging

q = QueryClient(logging.WARNING)

print(q.media_list(username="xxxAnn", per_page=100).entries[0])