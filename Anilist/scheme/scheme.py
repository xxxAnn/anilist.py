class Scheme:
    """    
    The main way to select fields to query in Anilist requests
    
    For example the following list of Schemes:

    .. code-block:: python

        Scheme().FieldA(id='$idVariable')
            .sub_schemes(
                Scheme().FieldB, 
                Scheme().FieldB.FieldC, 
                Scheme().FieldD
            )

    will be parsed into a query by the :class:`~.client.Client` as::
    
        FieldA (id: $idVariable) {
            FieldB {
                FieldC
            }
            FieldD
        }
    
    .. note::
        Schemes are parsed by :meth:`Client._create_query() <.client.Client._create_query>`
        Which is automatically called by :meth:`Query.search() <.query.Query.search>`

        Depending on the query parameters and the client type this will be wrapped into either a `query { }` block, a `query { Page { } }` block or a `mutation { }` block

    """

    def __init__(self):
        self._layers = []
        self._up = {}

    def sub_schemes(self, *schs):
        """Appends this :class:`~.Scheme` at the beginning of all of the :class:`~.Scheme`\s provided and returns them

        :param schs: List of :class:`~.Scheme`\s to append to this one
        :type schs: tuple[:class:`~.Scheme`], optional

        Example: 

        .. code-block:: python

            Scheme().FieldA.sub_schemes(
                Scheme().FieldB
                Scheme().FieldB.FieldC
                Scheme().FieldD
            )

            # is equivalent to

            [
                Scheme().FieldA,
                Scheme().FieldA.FieldB
                Scheme().FieldA.FieldB.FieldC
                Scheme().FieldA.FieldD
            ]
            
        """
        return [Scheme._combine(self, sch) for sch in schs] + [self]


    def __getattr__(self, k):
        return self[k]
    
    def __getitem__(self, k):
        self._layers.append(k)
        return self
    
    def __call__(self, **kwargs):
        d = dict(**kwargs)
        if d != {}:
            self._up[self._layers[-1]] = f"{self._layers[-1]} ({', '.join([f'{k}: {v}' for k, v in d.items()])})"
        return self
    
    def _replace_head(self, pat, r):
        self._layers[0] = str(self._layers[0]).replace(pat, r)
        tch = []
        for k, v in self._up.items():
            if k == pat:
                tch.append(k)

        for k in tch:
            self._up[r] = str(self._up.pop(k)).replace(pat, r)

        return self
    
    @classmethod
    def _construct(cls, *schs):
        d = {k: v for sch in schs for k, v in sch._up.items()}
        return construct_query_as_string(construct_query(list(schs)), d)
    
    @classmethod
    def _combine(cls, scha, schb):
        n = cls()
        n._layers = scha._layers + schb._layers
        n._up = scha._up | schb._up
        return n
    
def construct_query(schs: list[Scheme]):
    temp = {}

    for sch in schs:
        sch = sch._layers
        if not sch[0] in temp:
            temp[sch[0]] = {}
        for i in range(1, len(sch)):
            if not sch[i] in get_nest_list(get_numbers_up_to(i), temp, i, sch):
                get_nest_list(get_numbers_up_to(i), temp, i, sch)[sch[i]] = {}

    
    return temp


def construct_query_as_string(d, l, ss=""):
    if type(d) != dict:
        return str(d)
    
    s = ""

    for k, v in d.items():
        nk = k if k not in l else l[k]
        if v == {}:
            s = f"{s}{ss}{nk}\n"
        else:
            t = construct_query_as_string(v, l, f'{ss}  ')
            t = t[0:-1]
            s = f"{s}{ss}{nk} {{\n{t}\n{ss}}}\n"

    return s


def get_numbers_up_to(i):
    l = []
    n = i
    while n > 0:
        l.append(n)
        n -= 1
    
    return l

def get_nest_list(n, l, m, sch):
    prev = l
    for i in n:
        prev = prev[sch[m-i]]
    return prev
    
