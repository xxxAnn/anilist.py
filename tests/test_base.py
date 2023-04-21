import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../src'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))


from Anilist import QueryClient, Scheme
import logging

print(Scheme._construct(Scheme().A.B(k='$3'), Scheme().A.B.C, Scheme().A.B.C(k="$4").D))

q = QueryClient(logging.WARNING)

print(q.media_list(username="xxxAnn", per_page=100).entries[0])