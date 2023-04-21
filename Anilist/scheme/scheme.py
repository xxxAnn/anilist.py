class Scheme:

    def __init__(self):
        self._layers = []
        self._up = {}

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
    
    @classmethod
    def _construct(cls, *schs):
        return construct_query_as_string(construct_query(list(schs)), [sch._up for sch in schs])
    
REPLACE = "__SPECIAL_KEY_REPLACE__"

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
        if v == {}:
            s = f"{s}{ss}{REPLACE}{k}\n"
        else:
            t = construct_query_as_string(v, l, f'{ss}  ')
            t = t[0:-1]
            s = f"{s}{ss}{REPLACE}{k} {{\n{t}\n{ss}}}\n"

    if ss == "":
        for dic in l:
            for k, v in dic.items():
                s = s.replace(f"{REPLACE}{k}", f"{v}")
        s = s.replace(f"{REPLACE}", "")

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
    
