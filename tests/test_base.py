import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../src'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))


from Anilist import QueryClient, Scheme
import logging
from unittest import TestCase

class BaseTest(TestCase):

    def test_scheme(self):
        _ = Scheme._construct(Scheme().A.B(k='$3'), Scheme().A.B.C, Scheme().A.B.C(k="$4").D)
    
    def test_query(self):
        q = QueryClient(logging.WARNING)

        q.media_list(username="xxxAnn", per_page=100).entries[0]