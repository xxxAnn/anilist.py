from Anilist.scheme import Scheme
from unittest import TestCase

class InternalsTest(TestCase):

    def test_scheme(self):
        _ = Scheme._construct(Scheme().A.B(k='$3'), Scheme().A.B.C, Scheme().A.B.C(k="$4").D)